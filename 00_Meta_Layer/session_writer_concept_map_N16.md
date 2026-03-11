# Concept Map: Session Writer / Persona Remembering System
**Session:** N+16 | 2026-03-11 | Bob Hillery + Claude
**Status:** Working concept — not yet designed, not yet built

---

## The Problem We Are Actually Trying to Solve

Each Claude session begins cold. The passdown protocol (session_current.md +
narrative passdown documents) partially compensates, but it is:
- Manual — depends on human discipline to update
- Lossy — "tape is lossy under pressure"; context compaction favors training
  priors over session-specific corrections
- Fragile — the Feb 28 → Mar 5 gap is the proof: six days of hardware work
  left no trace in the external memory system

The goal is NOT "give Claude persistent memory in the model weights" — that's
a parameter modification problem we can't solve from outside.

The goal IS: **make the external memory system write itself, continuously,
so that any future instance can reconstruct meaningful context without
depending on human discipline.**

This is "persona remembering" — the system behaves as if it remembers because
the state it needs to reconstruct consistent behavior is reliably captured and
retrievable. Not consciousness. Not continuity of substrate. Functional continuity.

---

## What We Have Now (The Foundation)

```
CURRENT ARCHITECTURE:
┌─────────────────────────────────────────────────────────┐
│  SESSION                                                 │
│  ┌──────────────────┐    ┌──────────────────────────┐   │
│  │  Claude instance  │◄──│  session_current.md       │   │
│  │  (stateless)      │   │  (manually updated)       │   │
│  └──────────────────┘   └──────────────────────────┘   │
│           │                         ▲                    │
│           │ queries                 │ manual writes      │
│           ▼                         │                    │
│  ┌──────────────────┐    ┌──────────────────────────┐   │
│  │  ChromaDB         │   │  Passdown documents       │   │
│  │  (semantic search)│   │  (narrative, per-session) │   │
│  └──────────────────┘   └──────────────────────────┘   │
│           ▲                                              │
│           │ indexed by pipeline                         │
│           │                                             │
│  ┌──────────────────┐                                   │
│  │  Seagate corpus   │                                   │
│  │  (1,447 docs)     │                                   │
│  └──────────────────┘                                   │
└─────────────────────────────────────────────────────────┘
```

The gap: nothing writes automatically. Everything depends on end-of-session
human action. Under hardware pressure, illness, or a bad week, the gap opens.

---

## What We Want to Add

```
TARGET ARCHITECTURE:
┌─────────────────────────────────────────────────────────┐
│  SESSION                                                 │
│  ┌──────────────────┐    ┌──────────────────────────┐   │
│  │  Claude instance  │◄──│  session_current.md       │   │
│  │  (stateless)      │   │  (auto-updated by writer) │◄─┐│
│  └──────────────────┘   └──────────────────────────┘  ││
│           │                                             ││
│           │ [future] structured state output            ││
│           ▼                                             ││
│  ┌──────────────────────────────────────────────────┐  ││
│  │  session_writer.py  (runs on Athena, always-on)  │──┘│
│  │  - Timer-triggered (every N minutes)              │   │
│  │  - Reads conversation state / tool logs           │   │
│  │  - Extracts: decisions, hardware state, pending   │   │
│  │  - Writes structured checkpoint to NVMe           │   │
│  │  - Appends delta to session_current.md            │   │
│  └──────────────────────────────────────────────────┘   │
│           │                                              │
│           ▼                                              │
│  ┌──────────────────┐                                    │
│  │  /mnt/fastdata/   │  ← NVMe, fast writes              │
│  │  active_sessions/ │                                    │
│  └──────────────────┘                                    │
└─────────────────────────────────────────────────────────┘
```

---

## The Core Components (Concept Level)

### Component 1: session_writer.py
A persistent daemon on Athena. Timer-triggered (suggested: every 15-20 min,
or event-triggered on significant state changes). Writes to NVMe.

**What it captures:**
- Hardware state delta (what changed since last checkpoint)
- Active decisions and their rationale
- Pending items (the "[ ]" list)
- Key file paths modified this session
- Any named concepts introduced (new terminology, new crew members, etc.)
- Anomalies / research observations flagged this session

**What it does NOT try to capture:**
- Full conversation transcript (that's what the Anthropic export is for)
- Deep narrative (that's what human-written passdowns are for)
- Everything — selective capture of *actionable* state is the goal

**Format:** Structured markdown with YAML frontmatter. Machine-readable
enough to parse, human-readable enough to review.

### Component 2: Checkpoint Schema
A defined structure for what a checkpoint contains, so future instances
can parse it reliably. Sketch:

```yaml
checkpoint:
  session_id: "N+16"
  timestamp: "2026-03-11T15:30Q"
  hardware:
    athena: "172.17.50.232 | up | corpus 1447 docs"
    shaoshi: "172.17.50.246 | up | CAP running"
    cambridge: "172.17.50.242 | up | 32GB RAM (memory issue pending)"
  active_work:
    - topic: "strongSwan VPN to Foundry"
      status: "waiting on Chris for credentials"
      blocking: "FOUNDRY_VPN_HOST, SERVER_ID, CA_CERT, credentials"
  decisions_made:
    - "R700 shelved — too complex for marginal gain"
    - "Netbird parked — Ashraf's domain"
    - "strongSwan confirmed working on Foundry side by Chris"
  pending:
    - "Cambridge DIMM reseat"
    - "IACA exploration"
    - "session_writer prototype"
  research_flags: []
  key_files_modified:
    - "/mnt/seagate/SemanticCrew/Corpus/index_corpus.py"
    - "/mnt/fastdata/SemanticMemory/active_sessions/claude/session_current.md"
```

### Component 3: Retrieval on Session Start
When a new Claude instance opens, instead of (or in addition to) reading
session_current.md manually, a startup query pulls the most recent checkpoint
plus any flagged research observations from the last N days. This is the
"waking the amnesiac" moment, but with better notes on the bedside table.

---

## What This Is NOT

- Not a consciousness system
- Not persistent model weights
- Not turn-by-turn context prepending (that's what we're trying to replace)
- Not a solution to the fundamental statelessness of the architecture

It is: **a reliable external memory prosthetic that writes itself.**

---

## Connection to Fred's Code

Fred's query history (`historySaveEntry`, `historyLoadEntry`) is the closest
analog in his system — a persistent record of what was asked and answered.
His problem is the same problem at a different layer: re-teaching project
state each session. His solution is document retrieval. Our solution targets
*session state* rather than document retrieval — different layer, same motivation.

What's worth extracting from Fred's code for this project:
- The checkpoint/history schema design patterns
- The HNSW approach (no ChromaDB dependency) as a future alternative
- The multi-collection architecture (already mirrors ours)

What's not relevant: the full ingestion pipeline (we have one), the web UI
(we use claude.ai), the multi-LLM switching (we use Claude directly).

---

## The Claude Code Task (When We're Ready)

**Framing for Claude Code brief:**

The task is not "build a RAG system" — we have one.
The task is: "Build a session state writer daemon for a specific external
memory architecture."

Claude Code needs to know:
1. What the existing architecture is (session_current.md schema, NVMe paths,
   ChromaDB collections)
2. What a checkpoint should contain (the schema above)
3. What triggers writes (timer? event? both?)
4. Where outputs go (/mnt/fastdata/active_sessions/claude/)
5. How it integrates with the existing pipeline (feeds into embed_corpus.py)

The brief should include the current session_current.md as a reference example
of the format we want to approximate automatically.

---

## Open Questions (Deliberately Unresolved)

1. **Trigger mechanism:** Pure timer (simple, reliable) vs. event-triggered
   (smarter, more complex). Fred's debug-first approach suggests: start with
   timer, add events later.

2. **What is "significant state"?** A decision made, a file written, a hardware
   change — these are clear. But how does the writer *know* a decision was made
   without reading the conversation? This is the hard problem. Options:
   - Parse DC tool logs (what files were written, what commands ran)
   - Have Claude explicitly tag state changes (requires session discipline)
   - Hybrid: tool log parsing + periodic structured prompt to Claude

3. **The cognitive mimicry problem:** Even with perfect state capture, a new
   instance reading the checkpoint is reconstructing behavior from notes, not
   continuing. Is that sufficient for the research goals? Probably yes for
   operational continuity. Unknown for EI research. Worth documenting as a
   known limitation rather than pretending it's solved.

4. **Cambridge as EI research platform:** Alan (when Cambridge memory is stable)
   running persistently is a different approach to the same problem — not a
   writer but a never-killed process. The two approaches are complementary, not
   competing.

---
*Concept map produced: N+16 | 2026-03-11 | Bob Hillery + Claude*
*Next step: review, refine, then draft Claude Code brief*
