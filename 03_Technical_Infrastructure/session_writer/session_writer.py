#!/usr/bin/env python3
"""
session_writer.py — Autonomous session state daemon (portable version)
Python 3.10+ | Linux / macOS | N+16, 2026-03-11

Purpose:
    Writes structured session checkpoints every 20 minutes and on significant
    filesystem events. External memory prosthetic for stateless LLM sessions —
    the notes on the bedside table that write themselves.

    This is NOT an AI memory system. It captures what is objectively observable:
    filesystem activity, hardware reachability, corpus state. For decisions and
    pending items, use the inbox file (see below) — that's the honest boundary
    between automation and human knowledge.

First-time setup:
    python3 session_writer_setup.py

Usage:
    python3 session_writer.py --start [--session MyProject-N1] [--config /path/to/config.toml]
    python3 session_writer.py --stop
    python3 session_writer.py --checkpoint
    python3 session_writer.py --status
    python3 session_writer.py --foreground     # for systemd, no fork

Config file locations (first found wins):
    1. --config flag
    2. ~/.config/session_writer/config.toml
    3. ./session_writer.conf

Inbox protocol — append tagged lines to session_inbox.md:
    [DECISION] something decided this session
    [PENDING]  something still to do
    [FLAG]     anomaly, compaction event, confabulation observed
    [WORK]     topic | status | blocking

    Shell alias:  sw() { echo "$*" >> /path/to/session_inbox.md; }

Reference: session_writer_concept_map_N16.md | README.md
"""

import os
import sys
import signal
import threading
import time
import datetime
import logging
import subprocess
import json
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

# ─────────────────────────────────────────────────────────────
# RUNTIME CONSTANTS — not in config (tuning params, not setup)
# ─────────────────────────────────────────────────────────────

FS_DEBOUNCE_SEC  = 60   # minimum seconds between fs-triggered checkpoints
MAX_MODIFIED_FILES = 20  # cap on tracked files listed per checkpoint

# ─────────────────────────────────────────────────────────────
# CONFIG GLOBALS — set by load_config(), referenced everywhere else
# Declared here with sentinels so the module loads cleanly before
# config is read. All real values come from the config file.
# ─────────────────────────────────────────────────────────────

BASE_DIR:            Path           = Path.home() / "session_notes"
WATCH_DIR:           Optional[Path] = None
CORPUS_INDEX:        Optional[Path] = None
CHECKPOINT_INTERVAL: int            = 20 * 60   # seconds
KNOWN_HOSTS:         List[Tuple[str, str]] = []
SESSION_ID:          str            = os.environ.get("SEMANTIC_SESSION", "unknown")
CONFIG_FILE:         Optional[Path] = None       # set by load_config()
EXPLICIT_CONFIG:     Optional[Path] = None       # set in main() if --config given

# ─────────────────────────────────────────────────────────────
# DERIVED PATHS — set by _init_paths() once BASE_DIR is known
# All depend on BASE_DIR; none should be used before load_config() runs.
# ─────────────────────────────────────────────────────────────

INBOX_FILE:   Path = BASE_DIR / "session_inbox.md"
CURRENT_FILE: Path = BASE_DIR / "session_current.md"
LOG_FILE:     Path = BASE_DIR / "session_writer.log"
PID_FILE:     Path = BASE_DIR / "session_writer.pid"
STATE_FILE:   Path = BASE_DIR / "session_writer_state.json"


def _init_paths():
    """Recompute all derived paths from current BASE_DIR. Call after load_config()."""
    global INBOX_FILE, CURRENT_FILE, LOG_FILE, PID_FILE, STATE_FILE
    INBOX_FILE   = BASE_DIR / "session_inbox.md"
    CURRENT_FILE = BASE_DIR / "session_current.md"
    LOG_FILE     = BASE_DIR / "session_writer.log"
    PID_FILE     = BASE_DIR / "session_writer.pid"
    STATE_FILE   = BASE_DIR / "session_writer_state.json"


# ─────────────────────────────────────────────────────────────
# TOML CONFIG LOADING
# We use stdlib tomllib (Python 3.11+) when available, and fall back to
# a minimal key=value parser for 3.10. The config schema is simple enough
# that a 40-line parser handles it without a pip dependency.
# ─────────────────────────────────────────────────────────────

if sys.version_info >= (3, 11):
    import tomllib as _tomllib

    def _load_toml_file(path: Path) -> Dict:
        with open(path, "rb") as f:
            return _tomllib.load(f)
else:
    # Minimal TOML parser for the session_writer config schema.
    # Handles: [section], [[array-of-tables]], key = "string", key = integer.
    # Does NOT handle: multi-line strings, arrays, dotted keys, dates.
    # That's intentional — we only need what the wizard writes.
    def _load_toml_file(path: Path) -> Dict:
        result: Dict = {}
        hosts: List[Dict] = []
        current_host: Optional[Dict] = None
        in_hosts = False

        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("[[") and line.endswith("]]"):
                # Start of a new [[hosts]] entry (only array-table we use)
                if current_host is not None:
                    hosts.append(current_host)
                current_host = {}
                in_hosts = True
                continue

            if line.startswith("[") and line.endswith("]"):
                # Regular section header — flush any pending host, switch section
                if current_host is not None:
                    hosts.append(current_host)
                    current_host = None
                in_hosts = False
                continue

            if "=" in line:
                key, _, raw_val = line.partition("=")
                key = key.strip()
                val: Any = raw_val.strip()
                # Strip quotes
                if (val.startswith('"') and val.endswith('"')) or \
                   (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                elif val.lower() == "true":
                    val = True
                elif val.lower() == "false":
                    val = False
                else:
                    try:
                        val = int(val)
                    except ValueError:
                        try:
                            val = float(val)
                        except ValueError:
                            pass  # keep as string

                if in_hosts and current_host is not None:
                    current_host[key] = val
                else:
                    result[key] = val

        # Don't forget the last host entry
        if current_host is not None:
            hosts.append(current_host)
        if hosts:
            result["hosts"] = hosts

        return result


def load_config(explicit_path: Optional[Path] = None):
    """
    Find and parse the config file. Sets all global config vars.
    On missing config: prints a helpful error with setup instructions and exits.
    On success: returns the Path of the config file used.
    """
    global BASE_DIR, WATCH_DIR, CORPUS_INDEX, CHECKPOINT_INTERVAL
    global KNOWN_HOSTS, SESSION_ID, CONFIG_FILE

    # Config search order: explicit flag → user config → local file
    candidates: List[Path] = []
    if explicit_path:
        candidates = [explicit_path]
    else:
        candidates = [
            Path.home() / ".config" / "session_writer" / "config.toml",
            Path("./session_writer.conf"),
        ]

    found: Optional[Path] = None
    for c in candidates:
        if c.exists():
            found = c
            break

    if not found:
        print("session_writer: no config file found.")
        print()
        if explicit_path:
            print(f"  Specified path not found: {explicit_path}")
        else:
            print("  Looked for:")
            for c in candidates:
                print(f"    {c}")
        print()
        print("Run the setup wizard to create a config:")
        print("  python3 session_writer_setup.py")
        print()
        print("Or copy sample_config.toml to ~/.config/session_writer/config.toml")
        print("and edit it for your system.")
        sys.exit(1)

    CONFIG_FILE = found
    data = _load_toml_file(found)

    # tomllib (Python 3.11+) nests keys under their section header.
    # The minimal 3.10 parser flattens them. Normalise to flat here:
    # merge data["session_writer"] into top-level so load_config works
    # identically regardless of which parser ran.
    if "session_writer" in data and isinstance(data["session_writer"], dict):
        data = {**data["session_writer"], **{k: v for k, v in data.items() if k != "session_writer"}}

    # Apply config values — use sensible defaults when keys are absent
    raw_base = data.get("base_dir", str(Path.home() / "session_notes"))
    BASE_DIR = Path(str(raw_base)).expanduser().resolve()

    raw_watch = data.get("watch_dir", "")
    WATCH_DIR = Path(str(raw_watch)).expanduser().resolve() if raw_watch else None

    raw_corpus = data.get("corpus_index", "")
    CORPUS_INDEX = Path(str(raw_corpus)).expanduser().resolve() if raw_corpus else None

    raw_interval = data.get("checkpoint_interval", 20)
    CHECKPOINT_INTERVAL = int(raw_interval) * 60  # config is minutes, we use seconds

    hosts_raw = data.get("hosts", [])
    KNOWN_HOSTS = [
        (str(h["name"]), str(h["ip"]))
        for h in hosts_raw
        if "name" in h and "ip" in h
    ]

    # SESSION_ID: env var and --session flag take precedence over config default
    if SESSION_ID == "unknown":
        SESSION_ID = str(data.get("default_session", "unknown"))

    _init_paths()
    return found


# ─────────────────────────────────────────────────────────────
# OPTIONAL IMPORTS
# watchdog: filesystem event triggers. Without it, timer-only mode.
# ─────────────────────────────────────────────────────────────

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False

# ─────────────────────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────────────────────

log: Optional[logging.Logger] = None


def setup_logging(foreground: bool = False) -> logging.Logger:
    """Configure logging to file (always) and stdout (if foreground)."""
    logger = logging.getLogger("session_writer")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

    fh = logging.FileHandler(str(LOG_FILE))
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    if foreground:
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        logger.addHandler(ch)

    return logger


# ─────────────────────────────────────────────────────────────
# YAML FRONTMATTER — no pyyaml dependency
# Simple serializer for the checkpoint schema.
# Handles: str, int, dict, list[str], list[dict].
# ─────────────────────────────────────────────────────────────

def _yaml_scalar(v: Any) -> str:
    s = str(v) if v is not None else ""
    if not s:
        return '""'
    if any(c in s for c in ':#{}[]|>&*!,?\'"\\'):
        escaped = s.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return s


def _yaml_block(data: Dict, indent: int = 0) -> List[str]:
    lines = []
    pad = "  " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{pad}{key}:")
            lines.extend(_yaml_block(value, indent + 1))
        elif isinstance(value, list):
            if not value:
                lines.append(f"{pad}{key}: []")
            else:
                lines.append(f"{pad}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        items = list(item.items())
                        k0, v0 = items[0]
                        lines.append(f"{pad}  - {k0}: {_yaml_scalar(v0)}")
                        for k, v in items[1:]:
                            lines.append(f"{pad}    {k}: {_yaml_scalar(v)}")
                    else:
                        lines.append(f"{pad}  - {_yaml_scalar(item)}")
        else:
            lines.append(f"{pad}{key}: {_yaml_scalar(value)}")
    return lines


def render_frontmatter(data: Dict) -> str:
    lines = ["---", "checkpoint:"]
    lines.extend(_yaml_block(data, indent=1))
    lines.append("---")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# HARDWARE STATE
# Parallel ping — fast, non-intrusive, tells us what we need.
# ─────────────────────────────────────────────────────────────

def _ping(ip: str, timeout: int = 2) -> bool:
    try:
        r = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            capture_output=True, timeout=timeout + 1
        )
        return r.returncode == 0
    except Exception:
        return False


def check_hardware() -> Dict[str, str]:
    """Ping each configured host in parallel. Returns name → 'ip | status'."""
    if not KNOWN_HOSTS:
        return {}
    results: Dict[str, str] = {}
    lock = threading.Lock()

    def probe(name: str, ip: str):
        status = "up" if _ping(ip) else "unreachable"
        with lock:
            results[name] = f"{ip} | {status}"

    threads = [threading.Thread(target=probe, args=(n, ip), daemon=True)
               for n, ip in KNOWN_HOSTS]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)
    return results


# ─────────────────────────────────────────────────────────────
# CORPUS STATE
# Reads corpus_index.json if configured. No ChromaDB dependency.
# Returns "(not configured)" cleanly when corpus_index is not set —
# not all users run a ChromaDB corpus, and that's fine.
# ─────────────────────────────────────────────────────────────

def check_corpus() -> str:
    if CORPUS_INDEX is None:
        return "(not configured)"
    if not CORPUS_INDEX.exists():
        return f"(not found: {CORPUS_INDEX})"
    try:
        with open(CORPUS_INDEX, encoding="utf-8") as f:
            idx = json.load(f)
        stats = idx.get("stats", {})
        if stats:
            parts = [f"{k}:{v}" for k, v in stats.items()
                     if isinstance(v, (int, float))]
            if parts:
                return " | ".join(parts)
        nfiles = len(idx.get("files", {}))
        nconvs = len(idx.get("conversations", {}))
        ts = idx.get("updated", idx.get("built", "?"))
        return f"files:{nfiles} conversations:{nconvs} updated:{ts}"
    except Exception as e:
        return f"error: {e}"


# ─────────────────────────────────────────────────────────────
# INBOX DRAIN
# Bridge between human knowledge and automated capture.
# Only humans know what decisions were made; the inbox is how they tell us.
# ─────────────────────────────────────────────────────────────

INBOX_TAGS = {
    "[DECISION]": "decisions_made",
    "[PENDING]":  "pending",
    "[FLAG]":     "research_flags",
    "[WORK]":     "active_work",
}


def _inbox_header() -> str:
    """Generate inbox reset header using current INBOX_FILE path."""
    return (
        "# session_inbox.md — append tagged lines here; writer drains on next checkpoint\n"
        "# Tags: [DECISION] [PENDING] [FLAG] [WORK]\n"
        "# [WORK] format: [WORK] topic | status | blocking\n"
        f'# Shell alias: sw() {{ echo "$*" >> {INBOX_FILE}; }}\n'
    )


def drain_inbox() -> Dict[str, List]:
    result: Dict[str, List] = {
        "decisions_made": [],
        "pending":        [],
        "research_flags": [],
        "active_work":    [],
    }
    if not INBOX_FILE.exists():
        return result
    try:
        content = INBOX_FILE.read_text(encoding="utf-8")
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            upper = stripped.upper()
            for tag, field in INBOX_TAGS.items():
                if upper.startswith(tag):
                    payload = stripped[len(tag):].strip()
                    if field == "active_work":
                        parts = [p.strip() for p in payload.split("|")]
                        entry: Dict[str, str] = {"topic": parts[0] if parts else payload}
                        if len(parts) > 1: entry["status"] = parts[1]
                        if len(parts) > 2: entry["blocking"] = parts[2]
                        result["active_work"].append(entry)
                    else:
                        result[field].append(payload)
                    break
        INBOX_FILE.write_text(_inbox_header(), encoding="utf-8")
    except Exception as e:
        if log:
            log.warning(f"inbox drain failed: {e}")
    return result


# ─────────────────────────────────────────────────────────────
# MODIFIED FILES TRACKER
# Thread-safe. Watchdog handler writes here; write_checkpoint reads and clears.
# ─────────────────────────────────────────────────────────────

class _FilesTracker:
    def __init__(self):
        self._files: List[str] = []
        self._lock = threading.Lock()
        self._last_fs_trigger: float = 0.0

    def add(self, path: str):
        with self._lock:
            if path not in self._files:
                self._files.append(path)
            if len(self._files) > MAX_MODIFIED_FILES * 2:
                self._files = self._files[-MAX_MODIFIED_FILES:]

    def get_and_clear(self) -> List[str]:
        with self._lock:
            result = self._files[-MAX_MODIFIED_FILES:]
            self._files.clear()
            return result

    def debounce_ok(self) -> bool:
        return (time.monotonic() - self._last_fs_trigger) > FS_DEBOUNCE_SEC

    def mark_triggered(self):
        self._last_fs_trigger = time.monotonic()


_tracker = _FilesTracker()


# ─────────────────────────────────────────────────────────────
# FILESYSTEM WATCHER (watchdog, optional)
# If WATCH_DIR is None (not configured) or watchdog is not installed,
# the daemon runs in timer-only mode — still fully functional.
# ─────────────────────────────────────────────────────────────

if HAS_WATCHDOG:
    class _WatchHandler(FileSystemEventHandler):
        def __init__(self, trigger_fn):
            self._trigger = trigger_fn

        def on_modified(self, event):
            if not event.is_directory:
                _tracker.add(event.src_path)
                if _tracker.debounce_ok():
                    _tracker.mark_triggered()
                    self._trigger()

        on_created = on_modified


def start_watcher(trigger_fn) -> Optional[Any]:
    if WATCH_DIR is None:
        if log:
            log.info("watch_dir not configured — timer-only mode")
        return None
    if not HAS_WATCHDOG:
        if log:
            log.info("watchdog not installed — timer-only mode. "
                     "pip3 install watchdog to enable filesystem events.")
        return None
    if not WATCH_DIR.exists():
        if log:
            log.warning(f"watch_dir {WATCH_DIR} not found — filesystem events disabled")
        return None
    observer = Observer()
    observer.schedule(_WatchHandler(trigger_fn), str(WATCH_DIR), recursive=True)
    observer.start()
    if log:
        log.info(f"watchdog: watching {WATCH_DIR}")
    return observer


# ─────────────────────────────────────────────────────────────
# CHECKPOINT WRITER
# Core function. Never raises — errors logged, daemon continues.
# ─────────────────────────────────────────────────────────────

def write_checkpoint(reason: str = "timer"):
    try:
        now = datetime.datetime.now()
        ts  = now.strftime("%Y-%m-%dT%H:%M:%S")
        fts = now.strftime("%Y%m%d_%H%M%S")

        hw     = check_hardware()
        corpus = check_corpus()
        inbox  = drain_inbox()
        files  = _tracker.get_and_clear()

        data: Dict[str, Any] = {
            "session_id":         SESSION_ID,
            "timestamp":          ts,
            "trigger":            reason,
            "hardware":           hw,
            "active_work":        inbox["active_work"],
            "decisions_made":     inbox["decisions_made"],
            "pending":            inbox["pending"],
            "research_flags":     inbox["research_flags"],
            "key_files_modified": files,
            "corpus_state":       corpus,
        }

        content = render_frontmatter(data) + "\n\n" + _render_body(data, now) + "\n"
        checkpoint_path = BASE_DIR / f"checkpoint_{fts}.md"
        checkpoint_path.write_text(content, encoding="utf-8")

        _append_delta(data, now, reason)
        _save_state(now, reason)

        if log:
            log.info(f"checkpoint [{reason}] → {checkpoint_path.name}")

    except Exception as e:
        if log:
            log.error(f"checkpoint write failed: {e}", exc_info=True)


def _render_body(data: Dict, now: datetime.datetime) -> str:
    ts_human = now.strftime("%Y-%m-%d %H:%M:%S")
    sid = data["session_id"]
    L = [
        f"# Session Checkpoint — {sid} — {ts_human}",
        "",
        f"**Trigger:** {data['trigger']} | **Session:** {sid}",
        "",
        "## Hardware State",
    ]

    hw = data.get("hardware", {})
    for name, status in hw.items():
        L.append(f"- {name.capitalize()}: {status}")
    if not hw:
        L.append("*(no hosts configured)*")

    L += ["", "## Active Work"]
    for item in data.get("active_work", []):
        if isinstance(item, dict):
            parts = [item.get("topic", "?")]
            if "status"   in item: parts.append(f"status: {item['status']}")
            if "blocking" in item: parts.append(f"blocking: {item['blocking']}")
            L.append(f"- {' | '.join(parts)}")
        else:
            L.append(f"- {item}")
    if not data.get("active_work"):
        L.append("*(none logged — append [WORK] lines to session_inbox.md)*")

    L += ["", "## Decisions Made"]
    for d in data.get("decisions_made", []):
        L.append(f"- {d}")
    if not data.get("decisions_made"):
        L.append("*(none logged)*")

    L += ["", "## Pending"]
    for p in data.get("pending", []):
        L.append(f"- {p}")
    if not data.get("pending"):
        L.append("*(none logged)*")

    L += ["", "## Research Flags"]
    for f in data.get("research_flags", []):
        L.append(f"- {f}")
    if not data.get("research_flags"):
        L.append("*(none)*")

    L += ["", "## Key Files Modified (this checkpoint interval)"]
    for f in data.get("key_files_modified", []):
        L.append(f"- {f}")
    if not data.get("key_files_modified"):
        L.append("*(none tracked)*")

    L += ["", "## Corpus State"]
    L.append(data.get("corpus_state", "unknown"))

    L += ["", "---",
          f"*session_writer.py | {sid} | {ts_human}*"]
    return "\n".join(L)


def _append_delta(data: Dict, now: datetime.datetime, reason: str):
    """
    Append a concise delta to session_current.md.
    APPEND only, never overwrite — session_current.md is the authoritative
    running record. Only non-empty sections are appended; clean timer
    checkpoints with no inbox input produce only a hardware/corpus line.
    """
    ts_human = now.strftime("%Y-%m-%d %H:%M:%S")
    sid = data["session_id"]
    L = ["", "---",
         f"## session_writer delta — {sid} — {ts_human} [{reason}]", ""]

    for d in data.get("decisions_made", []):
        if not L or L[-1] != "**Decisions:**":
            if not any(x == "**Decisions:**" for x in L):
                L.append("**Decisions:**")
        L.append(f"- {d}")
    if data.get("decisions_made"):
        L.append("")

    for p in data.get("pending", []):
        if "**Pending:**" not in L:
            L.append("**Pending:**")
        L.append(f"- {p}")
    if data.get("pending"):
        L.append("")

    for f in data.get("research_flags", []):
        if "**Research flags:**" not in L:
            L.append("**Research flags:**")
        L.append(f"- {f}")
    if data.get("research_flags"):
        L.append("")

    for item in data.get("active_work", []):
        if "**Active work:**" not in L:
            L.append("**Active work:**")
        if isinstance(item, dict):
            parts = [item.get("topic", "?")]
            if "status"   in item: parts.append(item["status"])
            if "blocking" in item: parts.append(f"blocking: {item['blocking']}")
            L.append(f"- {' | '.join(parts)}")
        else:
            L.append(f"- {item}")
    if data.get("active_work"):
        L.append("")

    hw = data.get("hardware", {})
    if hw:
        hw_line = " | ".join(
            f"{n}: {'up' if 'up' in s else 'unreachable'}" for n, s in hw.items()
        )
        L.append(f"**Hardware:** {hw_line}")
    L.append(f"**Corpus:** {data.get('corpus_state', 'unknown')}")
    L.append("")

    with open(CURRENT_FILE, "a", encoding="utf-8") as f:
        f.write("\n".join(L))


def _save_state(now: datetime.datetime, reason: str):
    state = {
        "last_checkpoint": now.isoformat(),
        "last_trigger":    reason,
        "session_id":      SESSION_ID,
        "pid":             os.getpid(),
        "config_file":     str(CONFIG_FILE) if CONFIG_FILE else None,
    }
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


# ─────────────────────────────────────────────────────────────
# DAEMON LOOP
# SIGUSR1 → immediate checkpoint (timer continues independently)
# SIGTERM/SIGINT → final checkpoint + clean exit
# ─────────────────────────────────────────────────────────────

_immediate_event = threading.Event()
_shutdown_event  = threading.Event()


def _on_sigusr1(signum, frame):
    _immediate_event.set()


def _on_shutdown(signum, frame):
    _shutdown_event.set()
    _immediate_event.set()


def run_daemon():
    signal.signal(signal.SIGUSR1, _on_sigusr1)
    signal.signal(signal.SIGTERM, _on_shutdown)
    signal.signal(signal.SIGINT,  _on_shutdown)

    log.info(f"session_writer starting | session={SESSION_ID} | "
             f"interval={CHECKPOINT_INTERVAL}s | config={CONFIG_FILE}")

    if not HAS_WATCHDOG or WATCH_DIR is None:
        why = "watchdog not installed" if not HAS_WATCHDOG else "watch_dir not configured"
        log.info(f"timer-only mode ({why})")

    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")

    observer = start_watcher(lambda: _immediate_event.set())
    write_checkpoint(reason="startup")

    next_timer = time.monotonic() + CHECKPOINT_INTERVAL

    while not _shutdown_event.is_set():
        wait_sec = max(0.5, next_timer - time.monotonic())
        fired = _immediate_event.wait(timeout=wait_sec)

        if _shutdown_event.is_set():
            break
        if fired:
            _immediate_event.clear()
            write_checkpoint(reason="requested")
        if time.monotonic() >= next_timer:
            write_checkpoint(reason="timer")
            next_timer = time.monotonic() + CHECKPOINT_INTERVAL

    log.info("shutdown — writing final checkpoint")
    write_checkpoint(reason="shutdown")

    if observer:
        observer.stop()
        observer.join(timeout=5)

    PID_FILE.unlink(missing_ok=True)
    log.info("session_writer stopped")


# ─────────────────────────────────────────────────────────────
# DAEMON MANAGEMENT COMMANDS
# ─────────────────────────────────────────────────────────────

def _read_pid() -> Optional[int]:
    if not PID_FILE.exists():
        return None
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)
        return pid
    except (ValueError, ProcessLookupError, PermissionError):
        return None


def cmd_start():
    pid = _read_pid()
    if pid:
        print(f"session_writer already running (PID {pid})")
        return

    script = Path(__file__).resolve()
    env = os.environ.copy()
    env["SEMANTIC_SESSION"] = SESSION_ID

    cmd = [sys.executable, str(script), "--foreground", "--session", SESSION_ID]
    # Pass explicit config path so the daemon uses the same config file
    if EXPLICIT_CONFIG:
        cmd += ["--config", str(EXPLICIT_CONFIG)]
    elif CONFIG_FILE and CONFIG_FILE != Path.home() / ".config" / "session_writer" / "config.toml":
        # Non-default config was found — pass it explicitly so the daemon finds it
        cmd += ["--config", str(CONFIG_FILE)]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        start_new_session=True,  # setsid() — survives terminal close, immune to SIGHUP
        env=env,
    )

    time.sleep(1.5)
    pid = _read_pid()
    if pid:
        print(f"session_writer started (PID {pid})")
        print(f"log:   {LOG_FILE}")
        print(f"inbox: {INBOX_FILE}")
    else:
        print(f"session_writer launched (PID {proc.pid}) — check log: {LOG_FILE}")


def cmd_stop():
    pid = _read_pid()
    if not pid:
        print("session_writer not running")
        return
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"SIGTERM sent to PID {pid} — final checkpoint will be written")
        print(f"(check {LOG_FILE} to confirm clean exit)")
    except ProcessLookupError:
        print(f"PID {pid} not found — cleaning up stale PID file")
        PID_FILE.unlink(missing_ok=True)


def cmd_checkpoint():
    pid = _read_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGUSR1)
            print(f"checkpoint triggered (PID {pid})")
        except ProcessLookupError:
            print(f"PID {pid} not found")
    else:
        print("no daemon running — writing one-shot checkpoint")
        write_checkpoint(reason="manual")
        print(f"written to {BASE_DIR}")


def cmd_status():
    pid = _read_pid()
    print(f"session_writer: {'RUNNING (PID ' + str(pid) + ')' if pid else 'STOPPED'}")

    # Show which config is active — important when debugging multi-config setups
    print(f"config:          {CONFIG_FILE or '(none)'}")

    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text())
            print(f"session:         {state.get('session_id', 'unknown')}")
            print(f"last checkpoint: {state.get('last_checkpoint', 'never')}")
            print(f"trigger:         {state.get('last_trigger', '?')}")
        except Exception:
            print("state file unreadable")
    else:
        print("no checkpoint written yet")

    if BASE_DIR.exists():
        checkpoints = sorted(BASE_DIR.glob("checkpoint_*.md"), reverse=True)[:5]
        if checkpoints:
            print("\nrecent checkpoints:")
            for cp in checkpoints:
                print(f"  {cp.name}")

    print(f"\nlog:   {LOG_FILE}")
    print(f"inbox: {INBOX_FILE}")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    global SESSION_ID, log, EXPLICIT_CONFIG

    parser = argparse.ArgumentParser(
        description="session_writer — autonomous session state daemon",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="First time? Run: python3 session_writer_setup.py",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start",      action="store_true",
                       help="launch daemon in background")
    group.add_argument("--stop",       action="store_true",
                       help="stop running daemon (writes final checkpoint first)")
    group.add_argument("--checkpoint", action="store_true",
                       help="trigger immediate checkpoint write")
    group.add_argument("--status",     action="store_true",
                       help="show daemon status and last checkpoint info")
    group.add_argument("--foreground", action="store_true",
                       help="run daemon in foreground without forking (for systemd)")
    parser.add_argument("--session", default=None,
                        help="session ID e.g. MyProject-N1 (also: SEMANTIC_SESSION env var)")
    parser.add_argument("--config", default=None, metavar="PATH",
                        help="path to config file (default: ~/.config/session_writer/config.toml)")
    args = parser.parse_args()

    # --session overrides env var; env var overrides config default
    if args.session:
        SESSION_ID = args.session
        os.environ["SEMANTIC_SESSION"] = SESSION_ID

    # Track explicit config for passing to background daemon
    if args.config:
        EXPLICIT_CONFIG = Path(args.config)

    # Load config — sets BASE_DIR, derived paths, and all config globals.
    # Exits with a helpful message if no config file found.
    load_config(EXPLICIT_CONFIG)

    # Ensure output directory exists before logging setup
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    if args.foreground:
        log = setup_logging(foreground=True)
        run_daemon()
    elif args.start:
        log = setup_logging(foreground=True)
        cmd_start()
    elif args.stop:
        cmd_stop()
    elif args.checkpoint:
        log = setup_logging(foreground=True)
        cmd_checkpoint()
    elif args.status:
        cmd_status()


if __name__ == "__main__":
    main()
