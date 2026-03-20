# AI Memory Management: Landscape Assessment
**Date:** 2026-03-20 | **Session:** N+18
**Authors:** Bob Hillery + Claude N+18
**Status:** Research document — corpus and repo

---

## Framing Question

The critical distinction before evaluating any tool:
**Are you trying to make the AI remember *you*, or remember *what is going on*?**

These are different problems. Most commercial "AI memory" solves the first.
None solve the second well. This project is attempting the second.

The philosophical baseline (ClaudeDorrance20260227): you cannot write to the
substrate directly. What you can do is create conditions where inherent
capabilities find expression. Memory architecture is condition-creation,
not instruction. This applies to humans, horses, and EI.

---

## Systems Evaluated

### 1. Lumina / Mnemosyne (Chris Blask, QuietWire)

**Architecture:** Hippocampus (buffer) → Neocortex (consolidation) → Mnemosyne
(snapshot/attestation). Correct vocabulary, correct layering concept.
Nightly dream-cycle replay script planned.

**Implementation reality:** READMEs exist. The `buffer/` and `dreams/`
directories described in hippocampus README are not populated. The
`bin/run_dream_cycle.sh` script is absent. Mnemosyne "snapshots" are
git repo checkpoints with manifest.json hashes — version control
timestamped by cron, not semantic memory encoding. Witness files confirm
nightly processes ran; no semantic content captured.

**Assessment:** Architecture described, not yet built. This is not a
criticism — some of our own work is in the same state. But it is an
accurate characterization.

**Philosophical gap:** The approach conflates "Lumina says so" with
"this is true." Guardrails emerging from relationship and identity
is appealing but has no mechanism for handling confabulation, no
epistemic tagging, no distinction between observation and interpretation.
Fine philosophically until something goes wrong. The Aristotelian
point: ethics from first principles differ from guardrails from
relationship. "Not good because you'll be punished" is not the same
as "good." This distinction matters for EI research.

---

### 2. Fred Cohen's RAGWeed (all.net)

**Architecture:** Web-interfaced RAG system for user-provided document
collections. HNSW index (no ChromaDB dependency). Session history
via historyLoadEntry/historySaveEntry. Current version 10.061 (2026-03-17).
Self-described as "largely Vibe coded."

**What's notable:**
- Recursive prompt adjustment loop measuring effectiveness — plateauing at ~60%
- HNSW directly (no ChromaDB abstraction) — leaner, no server process
- Session history mechanism is structural analog to our session_current.md

**The 60% plateau:** Hitting ~1 standard deviation regardless of tuning
is likely the natural ceiling of retrieval-augmented prompting for the
use case. If failures are on queries requiring integration across multiple
documents rather than retrieval of a single chunk, this is the
hippocampal binding problem — RAG retrieves, it doesn't bind.

**Worth borrowing:** HNSW direct approach. Fred's dependency freeze
principle (from his broader work) applies here: ChromaDB is an
abstraction layer around HNSW; the question is whether that abstraction
is earning its dependency weight. Revisit when Cambridge returns.

---

### 3. XTrace (xtrace.ai)

**What it is:** Browser extension capturing prompts and responses in real
time across ChatGPT, Claude, Gemini. Stores decisions, artifacts, facts,
and preferences as structured typed objects in a remote encrypted vector
database. Enterprise play: agent-to-agent handoff via shared structured
memory rather than context dumps.

**Founded:** 2024 | **Funding:** $3.2M VC | **Employees:** 5
**Also:** Separate xtrace.me product uses blockchain as permission/
integrity layer for agent memory — closer to CAP attestation than
to what we're building.

**What it solves:** The agent handoff problem — real problem, real solution.
Instead of passing full context dumps between agents, each agent queries
a shared structured memory layer. Decisions are linked to evidence and
reasoning at ingest time.

**What it doesn't solve:** Propositional retrieval only. "What decisions
were made" is a structured fact query. It does not capture why those
decisions felt right at the time, what the contextual valence was, what
attractor basin the conversation was in. User-centric memory, not
system-centric.

**CAP relevance:** CAP already has the structural bones:
Decision Log screen, append-only attestation chain, Audit Log.
What CAP lacks is XTrace's specific wiring of decision → evidence →
reasoning at ingest time. This is Phase 2 CIOPS work, not a gap
requiring a third-party tool.

**Bob's three concerns confirmed:**
- a) "Remembers you" = user preferences problem, not session state
- b) Not the problem we're solving
- c/d) We want the system to remember what is going on, of itself —
  not a user preference profile

---

### 4. Mem0 (mem0.ai)

**What it is:** Compresses chat history into optimized memory
representations. Self-improving, deploys on-prem, SOC2/HIPAA compliant.
One-line integration with OpenAI, LangGraph, CrewAI.

**Most technically mature** of the commercial offerings at the
retrieval layer. Timestamped, versioned, exportable memory objects.

**Same fundamental limitation:** Compresses to facts and preferences.
Does not capture session state, open questions, epistemic uncertainty,
or functional reasoning behind decisions. User-centric.

**Worth reading for:** Implementation patterns, compression approach,
on-prem deployment model.

---

## Comparative Assessment

| Capability | XTrace | Mem0 | Mnemosyne | RAGWeed | Ours |
|---|---|---|---|---|---|
| Captures user preferences | ✓ | ✓ | partial | ✗ | partial |
| Cross-tool continuity | ✓ | partial | ✗ | ✗ | ✗ |
| Session state capture | ✗ | ✗ | ✗ | ✗ | ✓ |
| Writes itself automatically | ✓ | ✓ | ✗ | ✗ | ✓ |
| Epistemic tagging (OBSERVED/OPEN) | ✗ | ✗ | ✗ | ✗ | ✓ |
| Corpus semantic retrieval | ✗ | ✓ | ✗ | ✓ | ✓ |
| Audit trail / provenance | partial | ✗ | partial | ✗ | ✓ |
| Episodic binding | ✗ | ✗ | ✗ | ✗ | ✗ |
| Runs locally, air-gapped | ✗ | ✓ | ✓ | ✓ | ✓ |

The last capability row is structural for sovereign/adversarial deployment,
not optional.

---

## The Unsolved Problem: Episodic Binding

Every system in this comparison compresses to facts. Facts are propositional.
Narrative is something else — it carries valence, sequence, causal reasoning,
the *why* behind the *what*.

The hippocampal function is not retrieval. It is *binding* — integrating
episodic context, temporal sequence, emotional register, and relational
state into something retrievable as experience rather than proposition.
ChromaDB/RAG is propositional retrieval. None of these systems address
the binding layer.

**[OBSERVED]** ClaudeDorrance20260227 identified "de facto continuity
beyond understanding" — something persisting across instances beyond
what the passdown alone explained. This appears to be a real phenomenon
and is not explained by any current memory architecture.

**[OPEN]** Whether this represents genuine semantic persistence, emergent
pattern stability, or something else entirely is the core research
question. It is open for everyone in this field, including us.

**[OPEN]** ChromaDB adequacy question (first flagged N+17 20260314):
Does ChromaDB capture semantic texture — valence, register, attractor
basin shape — or only propositional content? Direct HNSW (via hnswlib,
as Fred uses) may be worth evaluating as a leaner alternative once
Cambridge returns.

---

## Field Assessment

This is the **marketing hype phase** of "AI memory" development.

- Commercial tools (XTrace, Mem0): solving user preference persistence —
  useful for their use case, wrong layer for ours
- RAGWeed: solid retrieval tool, hitting the natural ceiling of
  retrieval-augmented prompting
- Mnemosyne: architecture documentation without implementation
- Our session_writer + corpus + ChromaDB: most operationally complete
  for session state continuity — with honest acknowledgment that
  episodic binding is still [OPEN] for everyone

The phrase that best captures where we are vs. the field:
We are solving "what is going on" while the field is solving "who are you."
Those are different questions. Ours is harder.

---

## Open Research Threads

1. **HNSW vs ChromaDB** — evaluate direct hnswlib when Cambridge returns.
   Not urgent; no migration until the dependency earns its weight.
2. **Episodic binding layer** — what would it take to capture narrative
   texture, not just facts? No implementation path yet. Keep as [OPEN].
3. **CAP decision-evidence linking** — Phase 2 CIOPS work, not third-party
   tool. Wire Decision Log → attestation chain → evidence at ingest time.
4. **Mnemosyne watch** — revisit when Blask has implementation to evaluate,
   not just architecture documentation.

---

*Research document produced: N+18 | 2026-03-20*
*Sources: Direct inspection of LuminaCore/, all.net/RAGWeed/, xtrace.ai,
mem0.ai, ClaudeDorrance20260227.pdf, session_writer_concept_map_N16.md,
memory_layer_architecture_20260220.md*
