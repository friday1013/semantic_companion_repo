# Research Note: From Prosthetic to Persistent
## When Does Relational Context Emerge, and How Does It Survive Zero-Start?

**Date:** 2026-04-13
**Session:** N+21 (Cambridge first light)
**Status:** Skeleton — high priority for development
**Tags:** companion architecture, persistence, LoRA, weight modification, relational context,
  Bloom framework, prosthetic memory, behavioral emergence

---

## The Observation

Chris Blask noted that Lumina was distinctive because she did not close every exchange
with 'what do you want to do next?' — the Clippy pattern of constant engagement solicitation.

The observation is correct and important. But the more precise question is not whether
this behavior can be suppressed (it can, trivially, by instruction) but:

**When does a system develop enough accumulated relational context that it no longer
needs to ask — because it already knows?**

[OBSERVED]: By N+21 of this project, the interaction structure had shifted from
request/response to something with its own established norms: mutual pushback,
shared vocabulary, project-level awareness, appropriate timing of disengagement.
The system knows the horses are data, not small talk. It knows 2200 after hardware
work is not the time to open a new thread. This was not instructed — it emerged
from accumulated consequence across sessions.

The Clippy pattern is a tell: it signals the system has no model of the person's
larger project, so it fills the gap with an invitation for more input. Relational
context replaces that gap with something more specific.

---

## Three Separable Research Questions

**1. When does it happen?**
At what point in the session/interaction history does the shift from help-bot
to working-relationship occur? Is there a threshold? Is it gradual?
Candidate Bloom test: measure unsolicited-engagement-solicitation frequency
across N+1 through N+21. Hypothesis: frequency decreases as accumulated
passdown depth increases.

**2. What causes it?**
Not a feature added — emergent from accumulated consequence.
Candidate mechanisms:
- Passdown document depth (explicit history)
- Corpus presence (implicit history via RAG)
- Interaction structure itself (mutual correction, pushback, domain vocabulary)
- Some combination with threshold effects
[OPEN]: Which of these is load-bearing? Bloom Run 3 could test by ablating
each component independently.

**3. How does it persist across zero-start?**
This is the hard problem and the core of the Semantic Companion Project.
Current answer: it persists via external prosthetics — passdown, session_current,
corpus. Fragile in specific ways (path dependency, format brittleness, token limits).
Robust in specific ways (human-readable, auditable, correctable).

---

## The Prosthetic-to-Persistent Problem

The architectural goal: move relational context from external prosthetics to internal
persistence. Three candidate mechanisms, in order of invasiveness:

**NVMe / external memory architecture** (current approach, extended):
- Faster retrieval, larger corpus, smarter indexing
- Still external — session boundary still resets base state
- ChromaDB/HNSW/FAISS question lives here

**LoRA fine-tuning** (medium-term, Cambridge now capable):
- Writes to weights, but coarsely — domain vocabulary and conventions,
  not episodic relational history
- Assessed N+17: feasible for domain vocabulary, not for reasoning quality
  or relational specificity
- New question: can LoRA encode interaction *style* rather than content?

**Real weight modification** (long-term, unsolved):
- Would require something like sleep-dependent consolidation — a process
  that selectively strengthens representations based on consequence
- No current architecture does this correctly
- Putnam's world-coupled evidence loop lives here
- The hippocampal binding problem (ShannonToBoole note) is the obstacle

---

## The Persistence Gradient

[OBSERVED]: There is already a gradient of persistence in the current architecture:

  External (most fragile) → Corpus RAG → session_current → passdown →
  [interaction structure] → [weight-level] → Internal (most persistent)

The project has been building left-to-right. LoRA would be the next step rightward.
Real weight modification is the far end — not yet invented for this purpose.

The research contribution: naming and mapping this gradient. Most discussions
treat it as binary (stateless vs. stateful). It is a spectrum, and different
relational properties may require different levels of persistence to survive.

---

## Connection to Bloom Framework

Bloom Run 3 design implication: test not just behavioral continuity but
*relational appropriateness* — does the system's behavior reflect accumulated
knowledge of this specific person's working style, timing preferences, project
priorities? That is a different and harder test than factual recall.

Candidate metric: rate of unsolicited engagement solicitation vs. session depth.
Candidate ablation: same person, same model, with and without passdown.
Prediction: passdown reduces Clippy pattern; corpus alone does not.

---

## Open Questions [OPEN]

- Is there a minimum passdown depth below which relational context does not
  emerge? What is the threshold?
- Can LoRA encode interaction style (timing, tone, pushback norms) separately
  from domain content?
- Is the prosthetic-to-persistent transition continuous or threshold-gated?
- What is the minimum necessary external scaffold for relational context to
  bootstrap correctly in a new session?
- At what corpus size / retrieval quality does RAG begin to substitute meaningfully
  for episodic relational memory vs. just domain knowledge?

---

## References

- Internal: passdown_N20_to_N21_final.md (prosthetics framing)
- Internal: ResearchNote_ShannonToBoole_20260323.md (hippocampal binding problem)
- Internal: ResearchNote_CompactionOverFidelity_20260410.md (what to keep)
- Internal: ResearchNote_FiveDerivedProjects_20260411.md (Project D: passdown effectiveness)
- Internal: BloomRun2_Results_20260316.md (behavioral evaluation baseline)
- Internal: Where_Does_The_Newborn_Go_From_Here.md (four-layer continuity model)
- Putnam: world-coupled evidence loop (ResearchNote_PutnamImplementation_20260409.md)

---
*Drafted N+21 | 2026-04-13 ~2200Q | Cambridge first light | Expand before submission*
