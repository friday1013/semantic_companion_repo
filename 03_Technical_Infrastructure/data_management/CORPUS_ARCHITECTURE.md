# SemanticCrew Corpus Architecture
**Canonical reference** — read this before touching any corpus scripts  
Bob Hillery + Claude N+14 | 2026-02-28 | Athena

---

## Overview

Two-stage pipeline: **index** then **embed**.  
Always run index first, then embed. Never skip the index step.

```
index_corpus.py --update      # discover new files, update corpus_index.json
embed_corpus.py --update      # read index, embed new docs into ChromaDB
```

Both scripts live at: `/mnt/seagate/SemanticCrew/Corpus/`  
Run from that directory or with full path.

---

## File Locations

| What | Path |
|------|------|
| Index script | `/mnt/seagate/SemanticCrew/Corpus/index_corpus.py` |
| Embed script | `/mnt/seagate/SemanticCrew/Corpus/embed_corpus.py` |
| Corpus index JSON | `/mnt/fastdata/SemanticMemory/index/corpus_index.json` |
| ChromaDB (active) | `/mnt/fastdata/SemanticMemory/chromadb/` |
| ChromaDB (legacy) | `/mnt/fastdata/SemanticMemory/chroma/` — empty, ignore |
| Conversation vectors | `/mnt/fastdata/SemanticMemory/working_vectors/claude/` — separate DB, 2531 chunks |
| New files staging      | `/mnt/seagate/SemanticCrew/Commons/ProjectLibrary/` |
| Architecture docs      | `/mnt/seagate/SemanticCrew/Commons/Architecture/` |
| Academic papers | `/mnt/seagate/SemanticCrew/Commons/AITheory/Academic/` |

---

## Index Schema

`corpus_index.json` has this structure:
```json
{
  "version": "...",
  "built": "ISO timestamp",
  "updated": "ISO timestamp",
  "stats": { ... },
  "conversations": { "export_id": { ... } },
  "files": {
    "/absolute/path/to/file.pdf": {
      "path": "/absolute/path/to/file.pdf",
      "filename": "file.pdf",
      "extension": ".pdf",
      "size_bytes": 12345,
      "modified": "ISO timestamp",
      "hash": "16-char sha256 prefix",
      "category": "library",
      "indexed_at": "ISO timestamp"
    }
  }
}
```

**Critical:** `files` is a **dict keyed by path**, not a list.  
`conversations` is also a dict. Do not assume list format.

---

## ChromaDB Collections

Active DB at `/mnt/fastdata/SemanticMemory/chromadb/`:

| Collection | Contents | ~Docs (2026-03-09 N+16) |
|------------|----------|---------------------|
| `research` | Research/, Emergence/, Analysis/ — core theory | 437 |
| `crew_memory` | All crew Memory/ dirs — session state & passdowns | 25 |
| `conversations` | Conversation exports (summaries + metadata) | 35 |
| `library` | Broader SemanticCrew library files | 950 |
| **TOTAL** | | **1,447** |

Query the DB:
```bash
python3 embed_corpus.py --query "your search term"
python3 embed_corpus.py --stats
```

Or directly via `chroma_query.py` in the same directory.

---

## LIBRARY_DIRS (as of 2026-02-28)

Directories scanned by `index_corpus.py`. To add a new directory, edit
`LIBRARY_DIRS` in `index_corpus.py` AND document it here.

```python
SEAGATE / "Research"                    # core theory docs
SEAGATE / "Commons/AITheory"            # AI theory + Background/ + Academic/ + ClaudeConsciousness/ + Emergence/
                                        # N+16 2026-03-09: merged CambrianDevelopment/Infrastructure/AITheory/ here
                                        # 46 new unique docs added; CambrianDevelopment removed from indexing
SEAGATE / "Commons/Architecture"        # architecture docs [added N+14]
SEAGATE / "Commons/ProjectLibrary"      # project-wide library [moved from Claude/ProjectLibrary N+15]
SEAGATE / "Claude/Memory"               # session state & passdowns
SEAGATE / "Kusanagi/Memory"
SEAGATE / "Muninn/Memory"
SEAGATE / "Maigret/Memory"
SEAGATE / "Huginn/Memory"               # sparse — transitioning to PyGPT
# CambrianDevelopment: REMOVED from indexing N+16 2026-03-09
#   Retained as historical archive at SEAGATE / "CambrianDevelopment"
#   All unique content merged into Commons/AITheory/ before removal
FASTDATA / "active_sessions"            # all crew active session state
FASTDATA / "index"                      # corpus index, session registry
FASTDATA / "swap"                       # serialized intermediate states
```

---

## Conversations Pipeline

Conversation exports live at:  
`/mnt/seagate/SemanticCrew/Corpus/raw/conversations/`

Subdirectory structure:
```
raw/conversations/
  claude/          # Anthropic export dirs
  kusanagi/        # GPT conversation exports
  maigret/
```

Full conversation pass (expensive, ~30-45 min):
```bash
python3 embed_corpus.py   # full rebuild — re-embeds everything
```

Update only (fast):
```bash
python3 index_corpus.py --update
python3 embed_corpus.py --update
```

**When to run full rebuild:** After adding a new conversation export batch,
or if the ChromaDB becomes inconsistent. Otherwise `--update` is sufficient.

**Next scheduled full pass:** After adding Feb 2026 conversation exports.
Check `/mnt/fastdata/SemanticMemory/working_vectors/claude/` separately —
this is the PyGPT-managed vector store (2,531 chunks as of 2026-02-28),
distinct from the SemanticCrew corpus.

---

## Common Errors & Fixes

**"string indices must be integers"** in cmd_update:  
→ `files` dict accessed as list. Fixed in N+14. Should not recur.

**"0 new files found" after adding files:**  
→ You skipped `index_corpus.py --update`. The embed script reads the index,
not the filesystem. Always index first.

**ChromaDB at wrong path:**  
There are multiple chroma.sqlite3 files on Athena:
- `/mnt/fastdata/SemanticMemory/chromadb/` ← ACTIVE, use this
- `/mnt/fastdata/SemanticMemory/chroma/` ← empty legacy, ignore
- `/mnt/fastdata/SemanticMemory/working_vectors/*/` ← per-agent stores

**embed_corpus.py loads model from HuggingFace warning:**  
→ `You are sending unauthenticated requests to the HF Hub` — harmless,
model is cached locally after first run.

---

## UUID Schema — Conversations

The `conversations` dict in `corpus_index.json` is keyed by **Anthropic conversation UUID**
(e.g. `c066cbf5-184f-4986-88ff-1061ec5e5192`). This is the same UUID that appears in
your browser URL: `claude.ai/chat/<UUID>`.

Each entry looks like:
```json
{
  "uuid": "c066cbf5-184f-4986-88ff-1061ec5e5192",
  "name": "Semantic Companion session N+14",
  "created": "2026-02-28",
  "updated": "2026-02-28",
  "message_count": 47,
  "summary_preview": "First ~500 chars of first assistant response...",
  "source_export": "data-2026-02-28-16-20-52-batch-0000",
  "export_dir": "/mnt/seagate/SemanticCrew/Corpus/raw/conversations/claude/2026-02/data-2026-02-28-16-20-52-batch-0000"
}
```

**The URL UUID is the canonical identifier.** It is stable across browsers, desktop apps,
and systems as long as you are logged into the same Claude Pro account. It is what
Anthropic uses internally to anchor the conversation to your user record.

**N+n session URLs for reference:**
- N+14: `claude.ai/chat/c066cbf5-184f-4986-88ff-1061ec5e5192`
- N+15: `claude.ai/chat/18f2a044-9cd4-4957-b573-33bf79fa2e89`

**Note on "internal" Claude UUID:** The model instance does not have a UUID in the same
sense — there is no persistent identifier for a running inference. The chat URL UUID
is the conversation record, not the model. This is the correct anchor for session
continuity tracking.

---

## Adding New Conversation Exports (step by step)

1. Download export from claude.ai → Settings → Export Data
2. Unzip into: `raw/conversations/claude/YYYY-MM/<export-dir-name>/`
   - The export dir contains `conversations.json`, `memories.json`, etc.
   - Keep the .zip alongside for archival
3. For copy-paste transcripts (.txt, .md): place in `Claude/ProjectLibrary/`
   - **Not** in `raw/conversations/` — that tree is for Anthropic JSON exports only

4. Run from `/mnt/seagate/SemanticCrew/Corpus/`:
```bash
python3 index_corpus.py --update      # discovers new convs + library files
python3 embed_corpus.py --update      # embeds only new docs
python3 embed_corpus.py --stats       # verify counts
```

---

1. Place files in the appropriate seagate directory (see LIBRARY_DIRS above)
   - New Claude session docs → `Claude/ProjectLibrary/`
   - Academic papers → `Commons/AITheory/Academic/`
   - Architecture/design docs → `Commons/Architecture/`
   - Research theory → `Research/`

2. Run the update pipeline:
```bash
cd /mnt/seagate/SemanticCrew/Corpus
python3 index_corpus.py --update
python3 embed_corpus.py --update
```

3. Verify:
```bash
python3 embed_corpus.py --stats
```

---

## Adding New LIBRARY_DIRS

1. Edit `index_corpus.py`, add to `LIBRARY_DIRS` list
2. Update the LIBRARY_DIRS table in **this file**
3. Run `index_corpus.py --update` (will scan new dir, skip existing paths)
4. Run `embed_corpus.py --update`

---

*Last updated: 2026-03-04 | Claude N+15 | ProjectLibrary moved to Commons/ProjectLibrary*
