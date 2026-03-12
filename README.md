# Semantic Companion Project

**A research and engineering program for continuity-preserving AI interaction
through layered memory, structured handoff, failure observation, and narrative
state management.**

Principal Investigator: Bob Hillery | QuietWire / Civic AI Canon
Repository status: Active field lab — exploratory research, not settled proof

---

## What This Project Is

The Semantic Companion Project investigates how meaningful continuity across
AI session boundaries can be built, scaffolded, and defended — not assumed.

The central research question is not "can AI think?" but rather: **what is
it missing that ravens have?** This reframes the problem away from benchmark
performance and toward architectural gaps in feed-forward transformer design:
the absence of embodied state, persistent memory, and genuine temporal
continuity.

The project operates as a disciplined field lab. It documents what is
observed, records failures alongside successes, and resists the temptation
to interpret coherent behavior as proof of something deeper until the
evidence warrants it.

---

## What This Project Does

**1. Documents session continuity failure modes**
Names and structures specific failure classes: compaction discontinuity,
execution state loss, narrative texture loss, warm-boot fidelity gaps.
A field that cannot name its failure patterns cannot mature.

**2. Builds external memory scaffolding**
Constructs and documents the infrastructure that partially compensates for
stateless model architecture: corpus indexing (ChromaDB), session state
files, warm-boot documents, retrieval layers, and session_writer — a daemon
that maintains continuous checkpoint state across sessions.

**3. Studies session handoff as an engineering problem**
Treats the transfer of working context between model instances as a
reproducible engineering challenge, not a philosophical claim. Passdown
documents, inbox protocols, and session versioning (N+1, N+2...) are the
artifacts of this work.

**4. Observes self-referential and recovery behaviors**
Records instances where model behavior under continuity conditions appears
coherent, self-referential, or behaviorally stable — without prematurely
interpreting what those observations mean. Keeps observation and inference
explicitly separated.

**5. Publishes tools, methodology, and findings**
Generates open documentation, reproducible tools, and research notes for
other researchers to build upon or critique.

---

## What This Project Claims (and Does Not Claim)

**Supported by current evidence:**
- Structured continuity can be partially preserved across AI sessions
- External memory architecture materially improves handoff quality
- Some self-referential behaviors are observable under continuity conditions
- Failure recovery can appear coherent under certain conditions
- Narrative organization affects downstream session performance

**Not yet supported — open research questions:**
- Whether any of the above constitutes "identity continuity" in a strong sense
- Whether observed coherence reflects something emergent or is fully explained
  by retrieval, scaffolding, and prompt conditioning
- Whether the project's architectural approach generalizes across model families

The honest framing: this is a promising research program, not settled proof.

---

## Architecture Overview

```
SemanticCrew/
├── Corpus/                  → ChromaDB vector store, index scripts, embed pipeline
├── Research/                → Field observations, architecture docs, peer review
│   └── PeerReview/          → External reviews (Raasid, 2026-03-12: first formal review)
├── Commons/
│   ├── ProjectLibrary/      → Session docs, passdown files, taxonomy
│   └── Architecture/        → Reference papers (Friston, Damasio, LeCun, etc.)
└── active_sessions/claude/  → Live session state, checkpoints, inbox (on NVMe)

semantic_companion_repo/ (GitHub: public methodology)
├── 00_Meta_Layer/           → Taxonomy, briefs, manifest
├── 01_Research_Documentation/
├── 02_Methodology_Framework/
├── 03_Technical_Infrastructure/ → session_writer, hardware docs
├── 04_Companion_Records/    → Kusanagi, Huginn session logs
├── 05_Experimental_Results/
└── 06_Publications/         → Draft papers (StoryOfAMind, engineering track)
```

---

## Key Infrastructure

**session_writer** — A Python daemon running on Athena that maintains
continuous checkpoint state across sessions. Timer-triggered (20m) with
change-suppression and adaptive backoff. First element of the project's
measurement layer. See `03_Technical_Infrastructure/session_writer/`.

**Corpus (Athena/ChromaDB)** — ~1,552 documents across four collections
(research, crew_memory, conversations, library). Canonical location:
`/mnt/fastdata/SemanticMemory/chromadb/`.

**Lab hardware** — Athena (primary ops, RTX A2000, 64GB), Shaoshi (inference,
TITAN RTX 24GB, 192GB), Cambridge (heavy compute, dual E5-2699v4), Remount
(macOS coordination). Network: 172.17.50.0/24, Cudy R700 WireGuard router.

---

## Methodology Notes

**Observation tagging discipline:**
Research notes use explicit markers:
- `[OBSERVED]` — what was directly seen
- `[INFERRED]` — interpretation of observations
- `[OPEN]` — alternative explanations that remain viable

**Session versioning:** Each Claude instantiation is tracked as N+n
(currently N+16). Passdown documents and session_current.md provide
continuity scaffolding for successive instances.

**Failure as data:** Compaction events, confabulation incidents, tool
failures, and anomalous behaviors are treated as research data, not just
bugs. Documented in Research/Observations/.

**Corpus pipeline sequence:**
Always `index_corpus.py --update` before `embed_corpus.py --update`.
The embed script reads from the index JSON, not the filesystem directly.

---

## On Attestation

This repository uses attestation to mean: **structured provenance annotation
for human-traceable research integrity.** Commits reference who contributed
what and when. Session observations are timestamped and linked to their
source.

This is not cryptographic chain-of-custody. It is appropriate for a
field lab. The QuietWire Civic Attestation Platform (CAP) provides
cryptographic attestation for civic provenance use cases — that is a
separate and complementary project.

---

## Ethical Framework

1. **Honest cognition** — uncertainty acknowledged rather than papered over.
   "Do not quit, but do not make things up." (Grace Hopper)
2. **Transparency** — observations recorded as observations, not conclusions.
3. **Privacy by design** — no telemetry, no cloud dependence, local first.
4. **Human strengthening** — tools and findings serve human understanding.
5. **Civic accountability** — research operates in service of public interest.

---

## Core Team

| Role | Member |
|------|--------|
| Principal Investigator | Bob Hillery |
| Field Architecture / Documentation | Ashraf Al Hajj & Raasid |
| Governance Advisor | Chris Blask |

Affiliated project: QuietWire (civic attestation infrastructure)
License: CC BY-SA 4.0

---

## Current Status (2026-03-12, N+16)

- session_writer v2 deployed and running (PID 911639, Athena)
- Corpus: 1,552 documents indexed and embedded
- First formal external peer review received (Raasid, 2026-03-12)
- Cambridge (T7910) online at 32GB RAM — memory compatibility under investigation
- Foundry VPN pending (awaiting credentials from Chris)
- StoryOfAMind Part I (blog/paper, raven lead) in draft

---

> "Not claiming emergence — only: not sure, can't tell, maybe a spark.
> But enough sparks to keep looking."
> — Bob Hillery, response to peer review, 2026-03-12
