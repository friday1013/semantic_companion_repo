#!/usr/bin/env python3
"""
session_writer_setup.py — First-time setup wizard for session_writer
Python 3.10+ | Run once before first use.

Generates ~/.config/session_writer/config.toml with your paths and hosts.
Re-runnable: prompts before overwriting existing config.

Usage:
    python3 session_writer_setup.py
"""

import sys
import datetime
from pathlib import Path

CONFIG_DIR  = Path.home() / ".config" / "session_writer"
CONFIG_PATH = CONFIG_DIR / "config.toml"

# ─────────────────────────────────────────────────────────────
# Prompt helpers
# ─────────────────────────────────────────────────────────────

def ask(prompt_text: str, default: str = "") -> str:
    """Prompt user. Shows default in brackets; Enter keeps it."""
    if default:
        try:
            answer = input(f"  {prompt_text} [{default}]: ").strip()
        except EOFError:
            return default
        return answer if answer else default
    else:
        try:
            return input(f"  {prompt_text}: ").strip()
        except EOFError:
            return ""


def ask_path(prompt_text: str, default: str = "", must_be_dir: bool = False) -> str:
    """
    Prompt for a path. Expands ~ to absolute. Returns empty string if blank and
    no default. Optionally verifies the result is an existing directory.
    """
    raw = ask(prompt_text, default)
    if not raw:
        return ""
    expanded = str(Path(raw).expanduser().resolve())
    if must_be_dir and not Path(expanded).is_dir():
        # Non-fatal: just warn. The directory might not exist yet.
        print(f"    (note: {expanded} does not exist yet — will be created on first run)")
    return expanded


def ask_int(prompt_text: str, default: int) -> int:
    """Prompt for an integer with a default."""
    raw = ask(prompt_text, str(default))
    try:
        return int(raw)
    except ValueError:
        print(f"    (invalid, using default: {default})")
        return default


# ─────────────────────────────────────────────────────────────
# Config writer
# ─────────────────────────────────────────────────────────────

def write_config(
    project_name: str,
    base_dir: str,
    watch_dir: str,
    corpus_index: str,
    interval: int,
    default_session: str,
    hosts: list,
) -> str:
    """
    Render a commented TOML config file as a string.
    The comments are important — they make the file self-documenting
    for collaborators who haven't read the README.
    """
    today = datetime.date.today().isoformat()
    lines = [
        f"# session_writer config — generated {today}",
        "# Edit this file directly or re-run session_writer_setup.py",
        "# Docs: see README.md alongside session_writer.py",
        "",
        "[session_writer]",
        "",
        f'project_name = "{project_name}"',
        "",
        "# base_dir: where checkpoints, logs, and inbox are written",
        "# Must be a writable directory. Will be created if it doesn't exist.",
        f'base_dir = "{base_dir}"',
        "",
        "# watch_dir: filesystem directory to watch for activity",
        "# Leave empty to disable filesystem event triggers (timer-only mode).",
        f'watch_dir = "{watch_dir}"',
        "",
        "# corpus_index: path to a corpus_index.json file (optional)",
        "# Used by projects running ChromaDB/SemanticCrew corpus pipelines.",
        "# Leave empty if you don't use one — checkpoints will show '(not configured)'.",
        "# See: https://www.trychroma.com/ for ChromaDB setup.",
        f'corpus_index = "{corpus_index}"',
        "",
        "# checkpoint_interval: minutes between automatic timer checkpoints",
        f"checkpoint_interval = {interval}",
        "",
        "# default_session: shown in checkpoint headers when --session is not given",
        f'default_session = "{default_session}"',
        "",
    ]

    if hosts:
        lines.append("# hosts: machines to probe by ping at each checkpoint")
        lines.append("# Add one [[hosts]] block per machine.")
        for name, ip in hosts:
            lines += [
                "",
                "[[hosts]]",
                f'name = "{name}"',
                f'ip   = "{ip}"',
            ]
        lines.append("")
    else:
        lines += [
            "# hosts: machines to probe by ping at each checkpoint",
            "# Uncomment and add entries for any machines you want to monitor.",
            "# [[hosts]]",
            '# name = "myserver"',
            '# ip   = "192.168.1.100"',
            "",
        ]

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Main wizard
# ─────────────────────────────────────────────────────────────

def main():
    print()
    print("Session Writer — First-time Setup")
    print("=" * 34)
    print()

    # Check for existing config
    if CONFIG_PATH.exists():
        try:
            yn = input(f"  Config already exists at {CONFIG_PATH}\n"
                       "  Overwrite? [y/N]: ").strip().lower()
        except EOFError:
            yn = "n"
        if yn not in ("y", "yes"):
            print()
            print("Setup cancelled. Existing config unchanged.")
            print(f"To edit manually: {CONFIG_PATH}")
            print()
            return
        print()

    # Gather inputs
    print("Basic setup:")
    print()
    project_name = ask("Project / person name (used in log headers)")
    if not project_name:
        project_name = "My Project"

    default_base = str(Path.home() / "session_notes")
    base_dir = ask_path("Output directory for checkpoints", default_base)
    if not base_dir:
        base_dir = default_base

    print()
    print("Filesystem watching (optional):")
    watch_dir = ask_path(
        "Directory to watch for activity (blank to disable)",
        "",
    )

    print()
    print("Corpus tracking (optional — for ChromaDB/SemanticCrew users):")
    corpus_index = ask_path(
        "Path to corpus_index.json (blank to skip)",
        "",
    )

    print()
    print("Timing:")
    interval = ask_int("Checkpoint interval in minutes", 20)
    if interval < 1:
        interval = 20

    default_session = ask("Default session ID (e.g. MyProject-N1)", "Session-N1")

    print()
    print("Machines to monitor (ping check at each checkpoint):")
    print("  Press Enter with a blank name when done.")
    print()
    hosts = []
    while True:
        name = ask("  Machine name (or blank to finish)", "").strip()
        if not name:
            break
        ip = ask(f"  IP address for {name}", "").strip()
        if ip:
            hosts.append((name, ip))
            print(f"    added: {name} @ {ip}")
            print()
        else:
            print("    (no IP given — skipped)")
            print()

    # Write config
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    out_dir = Path(base_dir)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"  Warning: could not create {out_dir}: {e}")
        print("  Create it manually before starting the daemon.")

    config_text = write_config(
        project_name=project_name,
        base_dir=base_dir,
        watch_dir=watch_dir,
        corpus_index=corpus_index,
        interval=interval,
        default_session=default_session,
        hosts=hosts,
    )

    CONFIG_PATH.write_text(config_text, encoding="utf-8")

    inbox = out_dir / "session_inbox.md"

    print()
    print("─" * 40)
    print(f"Config written to: {CONFIG_PATH}")
    print()
    print("What to do next:")
    print()
    print(f"  1. Start the daemon:")
    print(f"       python3 session_writer.py --start --session {default_session}")
    print()
    print(f"  2. Check status:")
    print(f"       python3 session_writer.py --status")
    print()
    print(f"  3. Add this alias to ~/.bashrc for the session inbox:")
    print(f'       sw() {{ echo "$*" >> {inbox}; }}')
    print()
    print(f"  4. Use the inbox alias during sessions:")
    print(f"       sw [DECISION] we chose approach A over B")
    print(f"       sw [PENDING] follow up with Chris on credentials")
    print(f"       sw [FLAG] context compaction at 85% — observed bias toward priors")
    print(f"       sw [WORK] VPN setup | blocked | waiting on CA cert")
    print()
    print(f"  5. Trigger an immediate checkpoint any time:")
    print(f"       python3 session_writer.py --checkpoint")
    print()
    print(f"Checkpoints will appear in: {base_dir}")
    print(f"Running log: {out_dir / 'session_writer.log'}")
    print()


if __name__ == "__main__":
    main()
