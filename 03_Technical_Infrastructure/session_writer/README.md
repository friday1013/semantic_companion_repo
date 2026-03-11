# session_writer — Autonomous Session State Daemon
**Portable version | Python 3.10+ | Linux / macOS**
**Origin: Semantic Companion Project — N+16, 2026-03-11**

---

## What This Is

A daemon that writes structured session state checkpoints automatically throughout a working session — without requiring you to do anything at session end.

**The problem it solves:** Each LLM session starts cold. The standard workaround is manually updating a state file at the end of each session, but that requires discipline. Under deadline pressure, hardware failures, or a bad week, the gap opens and context is lost.

session_writer fills the gap automatically. It runs in the background and writes structured checkpoints every 20 minutes (and on filesystem events if you enable it). The next session has good notes on the bedside table whether or not you remembered to write them.

**What it captures automatically:**
- Filesystem activity (files modified in your project directory)
- Hardware reachability (ping-based probes of configured machines)
- Corpus/vector DB state (if configured)
- Timestamps and session identity

**What it cannot capture automatically** (honest limitation, not papered over):
- Decisions made during the session
- Pending items and blockers
- Research flags and anomalies

For these, use the inbox file — see [Inbox Protocol](#inbox-protocol).

**What it is not:** An AI memory system. A RAG system. A transcript parser. This is a reliable external note-taker that writes itself.

---

## Quick Start

```bash
# 1. Run setup wizard (once per machine)
python3 session_writer_setup.py

# 2. Start the daemon
python3 session_writer.py --start --session MyProject-N1

# 3. Check it's running
python3 session_writer.py --status

# 4. Stop it (writes final checkpoint first)
python3 session_writer.py --stop
```

---

## Installation

```bash
bash session_writer_install.sh           # basic install
bash session_writer_install.sh --systemd # also install systemd user service
```

The install script:
1. Checks Python 3.10+
2. Tries to install `watchdog` (filesystem events — optional)
3. Copies scripts to `~/bin/`
4. Runs setup wizard if no config file exists
5. Prints the shell alias to add to `~/.bashrc`

### Manual install (no script)

```bash
# Copy to ~/bin
cp session_writer.py session_writer_setup.py ~/bin/
chmod +x ~/bin/session_writer.py ~/bin/session_writer_setup.py

# Run setup wizard
python3 ~/bin/session_writer_setup.py

# Start
python3 ~/bin/session_writer.py --start --session MyProject-N1
```

---

## Setup Wizard

The wizard (`session_writer_setup.py`) generates your config file interactively:

```
$ python3 session_writer_setup.py

Session Writer — First-time Setup
==================================
  Project / person name: Chris Blask
  Output directory for checkpoints [~/session_notes]:
  Directory to watch for activity (blank to disable):
  Path to corpus_index.json (blank to skip):
  Checkpoint interval in minutes [20]:
  Default session ID [Session-N1]: QW-N1

  Machines to monitor:
    Machine name: Foundry
    IP address for Foundry: 99.236.24.231
    Machine name:            ← blank to finish

Config written to: /home/chris/.config/session_writer/config.toml
```

The wizard:
- Shows defaults in brackets — press Enter to accept
- Expands `~` paths to absolute paths
- Creates the output directory if it doesn't exist
- Writes a commented config file (human-readable/editable)
- Prints a "what to do next" summary
- Is re-runnable (prompts before overwriting)

---

## Config File

Location: `~/.config/session_writer/config.toml`
Alt location: `./session_writer.conf` (project-specific)
Override: `--config /path/to/config.toml`

```toml
# session_writer config — generated 2026-03-11
# Edit this file directly or re-run session_writer_setup.py

[session_writer]
project_name = "QuietWire / Chris Blask"
base_dir = "/home/chris/session_notes"

# watch_dir: leave empty to disable filesystem events (timer-only mode)
watch_dir = "/home/chris/Documents/QuietWire"

# corpus_index: path to corpus_index.json — leave empty if not using ChromaDB
corpus_index = ""

checkpoint_interval = 20     # minutes
default_session = "QW-N1"    # used when --session is not given

[[hosts]]
name = "Foundry"
ip   = "99.236.24.231"

[[hosts]]
name = "LocalBox"
ip   = "192.168.1.100"
```

Config is standard TOML. Python 3.11+ uses `tomllib`; 3.10 uses a built-in minimal parser — no pip dependency for config reading.

---

## Usage Reference

```bash
python3 session_writer.py --start [--session ID] [--config PATH]
python3 session_writer.py --stop
python3 session_writer.py --checkpoint
python3 session_writer.py --status
python3 session_writer.py --foreground   # for systemd or debugging
```

**`--start`** launches the daemon in the background. It survives terminal close (uses `setsid`). Writes initial checkpoint on startup.

**`--stop`** sends SIGTERM. The daemon writes a final checkpoint before exiting cleanly.

**`--checkpoint`** sends SIGUSR1 for an immediate checkpoint. If no daemon is running, writes a one-shot checkpoint and exits.

**`--status`** shows daemon state, config file in use, last checkpoint time, and recent checkpoint filenames.

**`--session`** sets the session ID shown in checkpoint headers. Also reads from `SEMANTIC_SESSION` environment variable. Config default is used when neither is set.

**`--config`** specifies a non-default config file path.

---

## Inbox Protocol

The inbox is how you tell the writer things it can't observe on its own.

**Inbox file location:** `{base_dir}/session_inbox.md`

**Tag format:**
```
[DECISION] R700 shelved — subnet complexity not worth the gain
[PENDING]  Follow up with Chris on VPN credentials
[FLAG]     Context compaction at 85% — observed bias toward training priors
[WORK]     VPN tunnel to Foundry | blocked | waiting on CA cert from Chris
```

**[WORK] pipe format:** `[WORK] topic | status | blocking`
All parts after the first `|` are optional.

**How it works:**
1. You append tagged lines to `session_inbox.md` any time during the session
2. On the next checkpoint, the writer reads and parses the inbox
3. Tagged items appear in the checkpoint's structured sections
4. The inbox file is reset (header comment restored)

**Shell alias** (add to `~/.bashrc`):
```bash
sw() { echo "$*" >> /path/to/session_notes/session_inbox.md; }
```

Then during a session:
```bash
sw [DECISION] switched from WireGuard to strongSwan — site-to-site requirement
sw [PENDING] reseat Cambridge DIMMs
sw [FLAG] confabulation observed — model inserted expected output without reading input
```

---

## Checkpoint Format

Checkpoints are written to `{base_dir}/checkpoint_YYYYMMDD_HHMMSS.md`.

Each file has YAML frontmatter (machine-parseable) followed by human-readable markdown:

```markdown
---
checkpoint:
  session_id: QW-N1
  timestamp: "2026-03-11T15:30:00"
  trigger: timer
  hardware:
    Foundry: "99.236.24.231 | up"
    LocalBox: "192.168.1.100 | unreachable"
  active_work:
    - topic: VPN tunnel to Foundry
      status: blocked
      blocking: CA cert from Chris
  decisions_made:
    - switched from WireGuard to strongSwan
  pending:
    - reseat Cambridge DIMMs
  research_flags: []
  key_files_modified:
    - /home/chris/Documents/QuietWire/vpn/ipsec.conf
  corpus_state: "(not configured)"
---

# Session Checkpoint — QW-N1 — 2026-03-11 15:30:00

**Trigger:** timer | **Session:** QW-N1
...
```

**Trigger values:** `startup` | `timer` | `requested` | `shutdown` | `manual`

---

## session_current.md

In addition to timestamped checkpoint files, the writer appends a concise delta block to `{base_dir}/session_current.md` on each checkpoint. This file is append-only — it never gets overwritten. Over the course of a session it becomes a running log.

To read back context at the start of a new session:
```bash
cat ~/session_notes/session_current.md
# or the most recent checkpoint:
ls -t ~/session_notes/checkpoint_*.md | head -1 | xargs cat
```

---

## Signal Interface

When the daemon is running:

| Signal | Effect |
|--------|--------|
| `SIGUSR1` | Immediate checkpoint (timer continues on its own schedule) |
| `SIGTERM` | Final checkpoint, clean exit |
| `SIGINT`  | Same as SIGTERM |

```bash
# Manual signals (alternative to --checkpoint / --stop)
kill -USR1 $(cat ~/session_notes/session_writer.pid)
kill -TERM $(cat ~/session_notes/session_writer.pid)
```

---

## Systemd User Service

After `bash session_writer_install.sh --systemd`:

```bash
# Start (set session via env var)
SEMANTIC_SESSION=QW-N1 systemctl --user start session_writer

# Enable to start automatically on login
systemctl --user enable session_writer

# Status and logs
systemctl --user status session_writer
journalctl --user -u session_writer -f

# Restart with new session ID
systemctl --user stop session_writer
SEMANTIC_SESSION=QW-N2 systemctl --user start session_writer
```

---

## Dependency Summary

| Feature | Requires | Without it |
|---------|----------|------------|
| Timer checkpoints | Python 3.10+ stdlib only | Always works |
| Filesystem events | `watchdog` (pip) | Timer-only mode |
| Config parsing | Python 3.11 `tomllib` or built-in parser | Always works |
| Hardware probes | `ping` (system command) | Reports "unreachable" |
| Corpus state | corpus_index.json at configured path | "(not configured)" |
| Inbox drain | inbox file exists | Empty inbox in checkpoint |

---

## Known Limitations

**What requires human input via the inbox:**
- Decisions made during the session
- What is genuinely pending or blocked
- Research flags, anomalies, and compaction events
- The narrative arc of a session (passdown documents handle this separately)

**Corpus state:**
The writer reads `corpus_index.json` to report corpus stats. This reflects the last index/embed pipeline run, not live vector DB state. Run your index/embed pipeline separately to keep it current.

**Hardware probes:**
ICMP ping only — not authenticated SSH. Reports reachability, not health or service status.

**The cognitive mimicry note:**
Even with reliable checkpoint writing, a new LLM instance reading the checkpoints is reconstructing behavior from notes, not continuing. The notes make that reconstruction better — they don't make it continuous. Documented here as a known limitation rather than pretended away.

---

## Files

| File | Purpose |
|------|---------|
| `session_writer.py` | Main daemon |
| `session_writer_setup.py` | First-time setup wizard |
| `session_writer_install.sh` | Install script |
| `README.md` | This file |
| `sample_config.toml` | Commented config example |

---

*session_writer portable | N+16 | 2026-03-11*
*Semantic Companion Project — Bob Hillery*
