#!/usr/bin/env python3
"""
SemanticCrew Corpus Indexer
Builds corpus_index.json from:
  1. Anthropic conversation exports (conversations.json)
  2. SemanticCrew library files on seagate

Output: /mnt/fastdata/SemanticMemory/index/corpus_index.json

Usage:
    python3 index_corpus.py              # full rebuild
    python3 index_corpus.py --update     # add new files only
    python3 index_corpus.py --stats      # show index stats

Bob Hillery + Claude N+9, 20260215
Updated: N+14, 2026-02-28 — added Claude/ProjectLibrary, Commons/Architecture
Updated: N+15, 2026-03-01 — scan_conversations now parses conversations.json to UUID-keyed
                             entries; cmd_update now saves new conversations to index;
                             cmd_rebuild uses consistent dict format throughout
"""

import json
import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────────

SEAGATE = Path("/mnt/seagate/SemanticCrew")
FASTDATA = Path("/mnt/fastdata/SemanticMemory")
INDEX_OUT = FASTDATA / "index" / "corpus_index.json"

# Conversation exports — auto-discovered from raw/conversations/
RAW_CONVERSATIONS = SEAGATE / "Corpus/raw/conversations"

# Library directories to index (recursive)
LIBRARY_DIRS = [
    SEAGATE / "Research",
    SEAGATE / "Commons/AITheory",
    SEAGATE / "Commons/Architecture",   # architecture docs (added N+14 2026-02-28)
    SEAGATE / "Commons/ProjectLibrary", # project-wide library files (moved from Claude/ProjectLibrary N+15 2026-03-04)
    SEAGATE / "Claude/Memory",
    SEAGATE / "Kusanagi/Memory",
    SEAGATE / "Muninn/Memory",
    SEAGATE / "Maigret/Memory",
    SEAGATE / "Huginn/Memory",   # sparse — Huginn deprecated via OpenWebUI, transitioning to PyGPT
    # CambrianDevelopment removed from indexing N+16 2026-03-09:
    # content merged into Commons/AITheory/ via rsync --ignore-existing
    # CambrianDevelopment retained as historical archive (not indexed)
    FASTDATA / "active_sessions",  # all crew active session state
    FASTDATA / "index",            # corpus index, session registry
    FASTDATA / "swap",             # serialized intermediate states
]

# File extensions to index
TEXT_EXTENSIONS = {".md", ".txt", ".odt", ".pdf", ".html", ".py", ".json",
                   ".yaml", ".yml", ".rtf", ".pages"}
SKIP_DIRS = {"__pycache__", ".git", "node_modules", "lost+found",
             "bloom-workspace", "working_vectors"}

# ── Helpers ────────────────────────────────────────────────────────────────────

def file_hash(path: Path) -> str:
    """SHA256 of file contents for change detection."""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()[:16]
    except Exception:
        return "error"

def categorize(path: Path) -> str:
    """Assign a category based on file path."""
    s = str(path).lower()
    if "cambriandev" in s or "cambrian" in s:
        return "cambrian_archive"
    if "aitheory" in s or "ai_theory" in s or "architecture" in s:
        return "ai_background"
    if "research" in s:
        return "research"
    if "memory" in s or "passdown" in s or "session" in s:
        return "crew_memory"
    if "threats" in s or "disinfo" in s or "tac" in s:
        return "threats"
    if "projectlibrary" in s or "project_library" in s:
        return "project_library"
    return "general"

# ── Index builders ─────────────────────────────────────────────────────────────

def scan_library(existing_paths: set) -> list:
    """Walk LIBRARY_DIRS and return list of new file dicts."""
    entries = []
    for lib_dir in LIBRARY_DIRS:
        if not lib_dir.exists():
            continue
        for root, dirs, files in os.walk(lib_dir):
            # Prune skip dirs in-place
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in files:
                fpath = Path(root) / fname
                if fpath.suffix.lower() not in TEXT_EXTENSIONS:
                    continue
                spath = str(fpath)
                if spath in existing_paths:
                    continue
                try:
                    stat = fpath.stat()
                    entries.append({
                        "path": spath,
                        "category": categorize(fpath),
                        "size": stat.st_size,
                        "mtime": datetime.fromtimestamp(
                            stat.st_mtime, tz=timezone.utc
                        ).isoformat(),
                        "hash": file_hash(fpath),
                    })
                except Exception as e:
                    print(f"  WARN: could not stat {spath}: {e}")
    return entries

def scan_conversations(existing_ids: set) -> dict:
    """
    Discover conversation export dirs, parse conversations.json files,
    and return a dict of new UUID-keyed conversation entries.

    The embed script expects conversations keyed by UUID with fields:
      name, summary_preview, message_count, updated, created,
      source_export, export_dir

    existing_ids: set of UUIDs already in the index (skip these).
    Returns: dict { uuid: conv_entry } for NEW conversations only.
    """
    new_entries = {}
    if not RAW_CONVERSATIONS.exists():
        return new_entries

    for root, dirs, files in os.walk(RAW_CONVERSATIONS):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if "conversations.json" not in files:
            continue

        conv_path = Path(root) / "conversations.json"
        export_dir = conv_path.parent.name

        try:
            with open(conv_path, encoding="utf-8", errors="replace") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  WARN: could not parse {conv_path}: {e}")
            continue

        # Anthropic export format: list of conversation objects
        if not isinstance(data, list):
            print(f"  WARN: unexpected format in {conv_path} (not a list)")
            continue

        for conv in data:
            uuid = conv.get("uuid") or conv.get("id", "")
            if not uuid or uuid in existing_ids:
                continue

            # Extract short preview from first assistant message
            summary = ""
            messages = conv.get("chat_messages") or conv.get("messages", [])
            for msg in messages:
                role = msg.get("sender") or msg.get("role", "")
                if role in ("assistant", "claude"):
                    content = msg.get("text") or msg.get("content", "")
                    if isinstance(content, list):
                        content = " ".join(
                            c.get("text", "") for c in content
                            if isinstance(c, dict)
                        )
                    summary = str(content)[:500]
                    break

            new_entries[uuid] = {
                "uuid": uuid,
                "name": conv.get("name") or conv.get("title", "Untitled"),
                "created": (conv.get("created_at") or conv.get("created", ""))[:10],
                "updated": (conv.get("updated_at") or conv.get("updated", ""))[:10],
                "message_count": len(messages),
                "summary_preview": summary,
                "source_export": export_dir,
                "export_dir": str(conv_path.parent),
            }

    return new_entries

# ── Main ───────────────────────────────────────────────────────────────────────

def load_index() -> dict:
    if INDEX_OUT.exists():
        with open(INDEX_OUT) as f:
            return json.load(f)
    return {"files": [], "conversations": [], "updated": None}

def save_index(index: dict):
    INDEX_OUT.parent.mkdir(parents=True, exist_ok=True)
    index["updated"] = datetime.now(tz=timezone.utc).isoformat()
    with open(INDEX_OUT, "w") as f:
        json.dump(index, f, indent=2)

def cmd_stats(index: dict):
    files = index.get("files", [])
    convs = index.get("conversations", [])
    cats = {}
    for f in files:
        c = f.get("category", "unknown")
        cats[c] = cats.get(c, 0) + 1
    print(f"\nCorpus Index Stats  ({index.get('updated','never')})")
    print(f"  Files:         {len(files)}")
    print(f"  Conversations: {len(convs)}")
    print("\n  By category:")
    for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"    {cat:30s} {n}")


def cmd_update(index: dict):
    # files is a dict keyed by path in the actual schema
    files_dict = index.get("files", {})
    if isinstance(files_dict, list):
        files_dict = {f["path"]: f for f in files_dict}
    existing_paths = set(files_dict.keys())

    convs = index.get("conversations", {})
    existing_ids = set(convs.keys()) if isinstance(convs, dict) else {c.get("id","") for c in convs}

    print(f"\nUPDATE: SemanticCrew Corpus Indexer")
    print(f"Time: {datetime.now(tz=timezone.utc).isoformat()}")
    print("=" * 60)

    print("\n[1] Scanning library directories for new files...")
    new_files = scan_library(existing_paths)
    print(f"    Found {len(new_files)} new files")
    for entry in new_files:
        p = entry["path"]
        files_dict[p] = {
            "path": p,
            "filename": Path(p).name,
            "extension": Path(p).suffix.lower(),
            "size_bytes": entry.get("size", 0),
            "modified": entry.get("mtime", ""),
            "hash": entry.get("hash", ""),
            "category": entry.get("category", "general"),
            "indexed_at": datetime.now(tz=timezone.utc).isoformat(),
        }
        print(f"    + {Path(p).name}")
    index["files"] = files_dict

    print("\n[2] Scanning for new conversation exports...")
    new_convs = scan_conversations(existing_ids)
    print(f"    Found {len(new_convs)} new conversations")
    if new_convs:
        convs_dict = index.get("conversations", {})
        if isinstance(convs_dict, list):
            convs_dict = {c.get("uuid", c.get("id", "")): c for c in convs_dict}
        convs_dict.update(new_convs)
        index["conversations"] = convs_dict
        for uuid, c in new_convs.items():
            print(f"    + {c['name'][:60]}  ({c['updated']})")

    save_index(index)
    print(f"\n[3] Index saved to {INDEX_OUT}")
    print(f"    Total files:         {len(index['files'])}")
    print(f"    Total conversations: {len(index.get('conversations', {}))}")


def cmd_rebuild():
    print(f"\nREBUILD: SemanticCrew Corpus Indexer")
    print(f"Time: {datetime.now(tz=timezone.utc).isoformat()}")
    print("=" * 60)
    index = {"files": {}, "conversations": {}}

    print("\n[1] Scanning all library directories...")
    new_files = scan_library(set())
    print(f"    Found {len(new_files)} files")
    files_dict = {}
    for entry in new_files:
        p = entry["path"]
        files_dict[p] = {
            "path": p,
            "filename": Path(p).name,
            "extension": Path(p).suffix.lower(),
            "size_bytes": entry.get("size", 0),
            "modified": entry.get("mtime", ""),
            "hash": entry.get("hash", ""),
            "category": entry.get("category", "general"),
            "indexed_at": datetime.now(tz=timezone.utc).isoformat(),
        }
    index["files"] = files_dict

    print("\n[2] Scanning conversation exports...")
    new_convs = scan_conversations(set())
    print(f"    Found {len(new_convs)} conversations")
    index["conversations"] = new_convs

    save_index(index)
    print(f"\n[3] Index saved → {INDEX_OUT}")
    print(f"    Total files:         {len(index['files'])}")
    print(f"    Total conversations: {len(index['conversations'])}")

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    index = load_index()

    if "--stats" in args:
        cmd_stats(index)
    elif "--update" in args:
        cmd_update(index)
    else:
        cmd_rebuild()
