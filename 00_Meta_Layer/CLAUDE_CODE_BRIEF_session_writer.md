# Claude Code Brief: session_writer.py
**Project:** Semantic Companion Project — SemanticCrew
**Date:** 2026-03-11 | Session N+16
**Prepared by:** Bob Hillery + Claude N+16
**Working directory:** /mnt/seagate/SemanticCrew/Research/Architecture/

---

## Read These Files First (in order)

1. `session_writer_concept_map_N16.md` — this directory — the full design concept
2. `/mnt/fastdata/SemanticMemory/active_sessions/claude/session_current.md`
   — the human-maintained state file this system will automate writing
3. `/mnt/seagate/SemanticCrew/Corpus/CORPUS_ARCHITECTURE.md`
   — the existing corpus pipeline this integrates with
4. `FC/10.8.53-Working.sh` lines 947-1010 — Fred Cohen's query history schema
   for reference only (pattern ideas, not code to copy)

---

## What This System Is

The Semantic Companion Project researches AI identity continuity and emergent
behavior across stateless LLM instantiations. Each Claude session starts cold.
We compensate with manually-written state documents (session_current.md) and
narrative passdown documents — but these depend on human discipline at
end-of-session. When sessions are interrupted (hardware work, compaction events,
illness, a bad week), the gap opens and context is lost.

The session_writer is a daemon that writes session state to NVMe automatically
throughout a session, so a future Claude instance can reconstruct useful context
without depending on end-of-session human action.

This is NOT a memory system in the AI/model weights sense. It is an external
memory prosthetic — a reliable note-taker that writes itself.

---

## The Task

Build `session_writer.py` — a Python daemon that runs on Athena (Ubuntu 24.04)
and writes structured session checkpoints to:
`/mnt/fastdata/SemanticMemory/active_sessions/claude/`

### Core behavior:
- Runs as a background daemon (systemd service or standalone)
- Timer-triggered: write a checkpoint every 20 minutes
- Also event-triggered: write immediately on significant filesystem events
  (files written to /mnt/seagate/SemanticCrew/, new tool logs, etc.)
- Each checkpoint is a structured markdown file with YAML frontmatter
- Also maintains/appends a running `session_current.md` delta

### What a checkpoint captures:
```yaml
checkpoint:
  session_id: ""          # e.g. "N+16" — read from env or config
  timestamp: ""
  hardware:
    athena: "172.17.50.232 | up | ..."
    shaoshi: "172.17.50.246 | ..."
    cambridge: "172.17.50.242 | ..."
  active_work:
    - topic: ""
      status: ""
      blocking: ""
  decisions_made: []        # strings — one per decision
  pending: []               # strings — open action items
  research_flags: []        # anomalies, compaction events, confabulation
  key_files_modified: []    # absolute paths, last N modified in session
  corpus_state: ""          # last known ChromaDB totals if available
```

### What a checkpoint does NOT try to capture:
- Full conversation transcript (Anthropic export handles that)
- Deep narrative (human-written passdowns handle that)
- Everything — selective capture of actionable state only

---

## Technical Constraints

- Python 3.10+ (Athena standard)
- No new pip dependencies if avoidable — prefer stdlib
  - Acceptable: `watchdog` for filesystem events (already may be installed)
  - Acceptable: `pyyaml` for YAML frontmatter (likely installed)
  - Check with: `pip3 show watchdog pyyaml`
- Output path: `/mnt/fastdata/SemanticMemory/active_sessions/claude/`
  - NVMe mount, fast writes, always available
  - Checkpoint files: `checkpoint_YYYYMMDD_HHMMSS.md`
  - Running state file: `session_current.md` (append delta, don't overwrite)
- Daemon should survive Ctrl-C gracefully (write final checkpoint on exit)
- Log to: `/mnt/fastdata/SemanticMemory/active_sessions/claude/session_writer.log`

---

## The Hard Problem (document, don't over-engineer)

The writer can reliably capture:
- Timestamps and file modification events (objective, from filesystem)
- Corpus state (query ChromaDB collection counts)
- Hardware reachability (ping/SSH checks)

The writer cannot reliably capture without human input:
- What decisions were made this session (not in filesystem)
- What is "pending" (not in filesystem)
- Research flags / anomalies (not in filesystem)

**Recommended approach:** Implement a simple structured input mechanism —
a watched "inbox" file where the human (or Claude via DC tool) can append
tagged lines that the writer picks up and folds into the next checkpoint:

```
# /mnt/fastdata/SemanticMemory/active_sessions/claude/session_inbox.md
[DECISION] R700 shelved — subnet complexity not worth gain
[PENDING] Cambridge DIMM reseat
[FLAG] Compaction interrupt at 89% — mid-response context loss observed
[WORK] strongSwan VPN to Foundry | waiting on credentials from Chris
```

The writer drains this inbox file into the next checkpoint and clears it.
This preserves the "write itself" goal while acknowledging what only a human
can know. The inbox can be written by:
- Bob directly in a terminal
- A future Claude DC tool call
- A simple alias: `sw() { echo "$*" >> /mnt/fastdata/SemanticMemory/active_sessions/claude/session_inbox.md; }`

---

## Success Criteria

1. `session_writer.py --start` launches daemon, writes initial checkpoint
2. `session_writer.py --checkpoint` triggers immediate checkpoint write
3. `session_writer.py --status` shows last checkpoint time and current state
4. `session_writer.py --stop` writes final checkpoint and exits cleanly
5. Timer fires every 20 minutes and writes checkpoint without human action
6. Filesystem event fires checkpoint when files change under /mnt/seagate/SemanticCrew/
7. Inbox drain works: lines in session_inbox.md appear in next checkpoint
8. session_current.md delta append works correctly (doesn't overwrite history)
9. Daemon survives 24+ hours without memory leak or zombie processes
10. All output is human-readable markdown (a future Claude instance must be
    able to read these files and reconstruct session context)

---

## What to Produce

1. `session_writer.py` — the daemon (well-commented, ~200-400 lines)
2. `session_writer_install.sh` — install script that:
   - Checks dependencies
   - Creates output directories if not present
   - Installs optional systemd service file
   - Creates the shell alias for session_inbox
3. `session_writer_README.md` — usage docs including the inbox tag format

Place all output in: `/mnt/seagate/SemanticCrew/Research/Architecture/session_writer/`
(create the directory)

---

## What NOT to Build

- Do not build a web UI
- Do not build a vector embedding pipeline (embed_corpus.py handles that)
- Do not try to parse Claude conversation transcripts in real-time
  (we don't have API access to the live conversation)
- Do not build a full RAG system (ChromaDB already exists)
- Do not over-engineer the "detect decisions" problem — the inbox solves it
  simply and reliably

---

## Reference: Existing Infrastructure

```
Athena filesystem:
  /mnt/seagate/SemanticCrew/        — main corpus tree (Seagate HDD)
  /mnt/fastdata/SemanticMemory/     — NVMe, fast I/O
    chromadb/                       — vector DB
    active_sessions/claude/         — session state files (target dir)
    working_vectors/claude/         — PyGPT vectors

Corpus pipeline (existing, do not replace):
  /mnt/seagate/SemanticCrew/Corpus/index_corpus.py   — indexes files → JSON
  /mnt/seagate/SemanticCrew/Corpus/embed_corpus.py   — embeds → ChromaDB
  Run sequence: index --update THEN embed --update
```

---

## Tone / Style Notes

This project values:
- **Honest uncertainty over confabulation** (Admiral Grace Hopper: don't quit,
  but don't make things up — document "I don't know" rather than inventing)
- **Architecture over scale** — simple, well-structured code beats clever
- **Debug-first** — start with timer-only, add filesystem events only after
  timer is stable
- Comments should explain *why*, not just *what*

---
*Brief prepared: N+16 | 2026-03-11*
*Working dir for Claude Code: /mnt/seagate/SemanticCrew/Research/Architecture/*
