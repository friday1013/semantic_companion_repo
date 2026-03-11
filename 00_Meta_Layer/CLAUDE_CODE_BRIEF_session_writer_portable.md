# Claude Code Brief: session_writer portable/exportable version
**Project:** Semantic Companion Project — SemanticCrew
**Date:** 2026-03-11 | Session N+16
**Prepared by:** Bob Hillery + Claude N+16
**Working directory:** /mnt/seagate/SemanticCrew/Research/Architecture/session_writer/

---

## Read These Files First (in order)

1. `session_writer.py` — this directory — the existing working daemon (BASE)
2. `session_writer_README.md` — this directory — existing usage docs
3. `../session_writer_concept_map_N16.md` — original design rationale

---

## Context

session_writer.py is a working daemon on Athena (Bob Hillery's lab). It writes
structured session checkpoints every 20 minutes to NVMe, drains a tagged inbox
file, and probes hardware hosts. It was built for one specific machine with
hardcoded paths and IPs in a CONFIG block at lines ~58-75.

Bob wants to share this with two collaborators (Chris Blask, Ashraf Al Hajj at
QuietWire) who run different systems with different paths and hostnames. The goal
is a version that works out of the box on any Linux/macOS system with a one-time
setup step.

---

## The Task

Produce a portable version of session_writer.py in a new subdirectory:
`session_writer_portable/`

### Three deliverables:

**1. session_writer.py** (modified from existing)
Replace the hardcoded CONFIG block with config file reading. All 6 hardcoded
items become config keys:
- BASE_DIR (output path for checkpoints and inbox)
- WATCH_DIR (filesystem path to watch — optional, timer-only if absent)
- CORPUS_INDEX (path to corpus index — optional, skipped if absent)
- CHECKPOINT_INTERVAL (default 20 min)
- KNOWN_HOSTS (list of name:ip pairs to probe)
- SESSION_ID default (read from config, overridden by --session flag or env var)

Config file location (in priority order):
1. Path specified by --config flag
2. `~/.config/session_writer/config.toml` (user-level, preferred)
3. `./session_writer.conf` (local, for project-specific use)

Use Python stdlib `tomllib` (Python 3.11+) with fallback to manual key=value
parsing for Python 3.10 compatibility. Do NOT add toml as a pip dependency —
implement a minimal parser for the simple flat+list structure needed.

**2. session_writer_setup.py** (new — interactive setup wizard)
A standalone script that generates the config file. Run once on first install.

```
$ python3 session_writer_setup.py

Session Writer — First-time Setup
==================================
Project/person name: Chris Blask
Output directory for checkpoints [~/session_notes/]:
Directory to watch for filesystem events (leave blank to disable):
Vector DB index path (leave blank to skip corpus tracking):
Checkpoint interval in minutes [20]:

Machines to monitor (press Enter when done):
  Name: Foundry   IP: 99.236.24.231
  Name: [Enter]

Config written to: /home/chris/.config/session_writer/config.toml

To start: python3 session_writer.py --start --session MyProject-N1
Inbox:    /home/chris/session_notes/session_inbox.md
Alias:    sw() { echo "$*" >> /home/chris/session_notes/session_inbox.md; }
```

The wizard should:
- Show defaults in brackets, accept Enter to keep default
- Expand ~ paths to absolute
- Create output directory if it doesn't exist
- Write a commented config file so it's human-readable/editable
- Print a short "what to do next" summary at the end
- Be re-runnable (prompts to overwrite if config exists)

**3. session_writer_install.sh** (updated from existing)
Update the existing install script to:
- Call session_writer_setup.py if no config file found
- Otherwise, skip setup (idempotent)
- Install watchdog if available (pip3 install watchdog --break-system-packages)
- Print the shell alias to add to ~/.bashrc (don't write it automatically)
- Offer optional systemd user service install (--systemd flag, same as before)

---

## Config file format

Simple TOML-compatible but parseable with stdlib. Example output from wizard:

```toml
# session_writer config — generated 2026-03-11
# Edit this file directly or re-run session_writer_setup.py

[session_writer]
project_name = "QuietWire / Chris Blask"
base_dir = "/home/chris/session_notes"
watch_dir = "/home/chris/Documents/QuietWire"
corpus_index = ""
checkpoint_interval = 20
default_session = "QW-N1"

[[hosts]]
name = "foundry"
ip = "99.236.24.231"

[[hosts]]
name = "localbox"
ip = "192.168.1.100"
```

The minimal parser only needs to handle:
- `[section]` headers (ignore, read all keys flat)
- `[[hosts]]` as a signal to start a new host entry
- `key = "value"` and `key = integer`
- `#` comments (skip)
- Empty lines (skip)

---

## Vector DB / Corpus state handling

The existing code queries a ChromaDB corpus_index.json. In the portable version:

- If `corpus_index` is empty or file doesn't exist: checkpoint shows
  `corpus_state: "(not configured)"` — no error, no crash
- If corpus_index exists: read it and report file count and last-updated
  timestamp as before
- Add a comment in the config file explaining what this field is for and
  pointing to ChromaDB docs

Do NOT add ChromaDB as a dependency. The index JSON read is stdlib file I/O.

---

## What NOT to change

- The checkpoint format (YAML frontmatter + markdown body) — keep identical
- The inbox drain logic and tag vocabulary ([DECISION], [PENDING], [FLAG], [WORK])
- The daemon mechanics (--start, --stop, --status, --checkpoint, --foreground)
- The session_current.md append/delta logic
- The watchdog optional-import pattern (timer-only fallback)
- The "honest uncertainty" design principle — document what can't be captured

---

## Packaging output

After building the portable version in `session_writer_portable/`, also produce:

`session_writer_portable.zip` at:
`/mnt/seagate/SemanticCrew/Research/Architecture/session_writer_portable.zip`

Zip contents (flat — no nested project dir):
- session_writer.py
- session_writer_setup.py
- session_writer_install.sh
- README.md (update from existing to cover the setup wizard)
- sample_config.toml (a commented example with placeholder values)

The zip should be self-contained: unzip, run install.sh, done.

---

## Success criteria

1. `python3 session_writer_setup.py` runs interactively, writes valid config
2. `python3 session_writer.py --start` reads config, starts daemon without error
3. On a machine with no config file, `--start` prints a helpful error pointing
   to the setup wizard (does not crash with a traceback)
4. On a machine where corpus_index is absent, checkpoint shows "(not configured)"
   not an exception
5. `--status` shows config file path in its output (so user knows which config
   is active)
6. All existing Athena functionality still works (config file path
   ~/.config/session_writer/config.toml on Athena can be pre-populated)
7. Zip is valid and contains all 5 files

---

## Tone / style notes (same as original brief)

- Stdlib-first. Minimal dependencies.
- Comments explain why, not just what.
- Honest uncertainty: document limitations rather than over-engineer around them.
- The setup wizard should feel friendly, not like an enterprise installer.
  Short prompts, sensible defaults, clear output.

---
*Brief prepared: N+16 | 2026-03-11*
*Base code: session_writer/session_writer.py (835 lines, working)*
