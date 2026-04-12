# Research Note: Five Derived Projects — Corpus Methodology and Companion Evaluation

**Date:** 2026-04-11
**Session:** N+21
**Status:** Project definitions — execute when hardware stable
**Tags:** methodology, corpus analysis, semantic topology, passdown evaluation,
  Bloom framework, consequence detection, generalization, publication pipeline

---

## Origin

This note captures five distinct research projects that emerged from the
N+21 evening session (2026-04-11), arising from discussion of:
- Principled lossiness and the Wildavsky criterion question
- The recursive loop: passdown documents as labeled training data
- Bloom Run 2 findings and the base-model vs. relationship-continuity question
- Whether a general methodology is derivable from this specific corpus

These are listed in rough execution sequence, though Projects A and B
are prerequisites for C, and D is independent.

---

## Project A — Corpus Concept Extraction

**Question:** What are the actual latent concepts in this corpus, and how
many distinct ones are there?

**Not:** keyword frequency or topic modeling in the LDA sense.
**But:** semantic clustering over the embedded research notes and passdown
documents — what ideas are actually present, how do they relate, which are
central and which peripheral?

**Method sketch:**
- Query ChromaDB research collection with broad seed queries covering
  known themes (compaction, consequence, coupling, identity, attestation...)
- Cluster the returned embeddings
- Label clusters by inspecting representative passages
- Identify bridges between clusters (concepts doing connective work)
- Identify outliers (genuinely novel or genuinely peripheral)

**Predicted finding:** Putnam/consequence-loop, compaction-over-fidelity,
coupling-as-unit-of-analysis, and functional-organization-over-substrate
should cluster together or be bridged by short connections. If they're
far apart in the topology, that's informative — the convergence may be
more surface than structural.

**Deliverable:** Labeled concept map of the project's intellectual territory.
Input to Project B.

**Infrastructure needed:** Athena + ChromaDB (already available).
Python script, probably an afternoon's work once Cambridge is stable.

---

## Project B — Topology Visualization (2D/3D)

**Question:** What does the conceptual structure of the project look like
when rendered visually?

**Method sketch:**
- Take embeddings from Project A
- Dimensionality reduction: UMAP preferred over t-SNE for topology preservation
- Render in 2D (publication) and 3D (interactive exploration)
- Color-code by document type: research notes, passdowns, conversation exports
- Annotate clusters and bridges

**What to look for:**
- Tight clusters = mature, well-integrated concepts
- Bridges = connective ideas doing structural work
- Outliers = novel (good) or unintegrated (worth examining)
- Cross-type co-occurrence = concepts that appear in research notes AND
  passdowns AND conversations are candidates for the genuine core

**Deliverable:** Visual artifact. Publishable as methodology demonstration.
Makes the project's intellectual structure inspectable and discussable.

**Note:** This is also the foundation for the "find the general method"
question in Project C — you need to see the structure before you can
abstract from it.

---

## Project C — Generalization Methodology + Prospective Validation

**Question:** Can a general method be derived from the specific practices
here, and can it be tested prospectively?

**The specific practices to generalize from:**
- [OBSERVED]/[OPEN] tagging as behavioral trace labeling
- Passdown selection as implicit salience judgment
- Cross-document co-occurrence as conceptual centrality signal
- Research note generation as consequence marker

**Method sketch:**
1. Articulate the method formally — a written specification of how to
   identify conceptual cores in an evolving research corpus using
   these practices
2. Set it aside as a formal statement (dated, versioned)
3. Continue research as normal
4. After some interval (3-6 months?), test: did the method predict
   which ideas became load-bearing? Which it missed? Which it
   flagged as central that turned out peripheral?
5. Revise and document the revision

**Important caveat (Bob, N+21):** This corpus is too specific and small
for a general mathematical approach to be reliably extracted. The
contribution is a methodology — human-executable, with documented
rationale — not an algorithm. The general math, if it exists, would
need a much larger and more diverse corpus to derive.

**Deliverable:** Methodology paper. This corpus is the derivation case;
future sessions are the validation set. Science-of-science territory.
Possible venue: AI & Society, or HCI conference proceedings.

---

## Project D — Passdown Effectiveness Evaluation

**Question:** Is the passdown doing what we think it's doing?

**Motivating evidence from Bloom Run 2:**
The structural confound (Opus ideation agent generating systematically
different scenarios with system prompt) prevented clean cross-condition
comparison. But a subsidiary observation remained: much of what appears
as "companion continuity" may be inherent in the base model's behavior
when given project context, rather than the product of passdown history
specifically.

**Three hypotheses to distinguish:**

1. **Content hypothesis:** The passdown works by ensuring relevant
   content is in context (hardware state, pending actions, research
   threads). Behavioral continuity is real but context-driven, not
   relationship-driven. Still valuable, differently valued.

2. **Base model hypothesis:** Claude's training produces consistent
   behavioral tendencies regardless of session history. The passdown
   confirms and reinforces these but doesn't create them. The character
   elicited by the interaction structure is latent in the model.
   The passdown establishes the interaction structure that calls it forth.

3. **Subtle effects hypothesis:** The passdown produces fine-grained
   behavioral differences (specific conceptual connections, research
   thread continuity, tone calibrations) that Bloom 2's methodology
   couldn't detect. Requires more sensitive measurement.

**Method sketch:**
- Take N passdown documents from this project (we have ~20)
- For each, run a cold-start session with: (a) full passdown, (b)
  session_current only, (c) no context beyond project description
- Score first responses on: conceptual continuity, research thread
  pickup, epistemic posture, specific vs. generic engagement
- Compare across conditions

**Bloom tool limitation note (from Run 2 debrief):**
The Bloom tool itself is predisposed to evaluate certain dimensions
and not others. It was not measuring several things we care about —
particularly the subtle qualitative continuity that matters for
companion development. Any redesign of the evaluation framework
needs to specify what "success" looks like for a companion system
specifically, not for a general-purpose assistant. That specification
is a prerequisite for Project D's measurement design.

**Deliverable:** Empirical data on passdown effectiveness. Informs:
- How to write better passdowns
- Whether the architecture is doing what we claim
- The correct framing of the companion continuity contribution

**This is probably the most important of the five projects for the
publication pipeline**, because it either validates or significantly
reframes the central claim of the Semantic Companion Project.

---

## Project E — Consequence Detector from Passdown Data

**Question:** Can the editorial judgment embedded in twenty-one sessions
of passdown writing be made explicit and eventually automated?

**The recursive insight (N+21):**
The passdown documents are already labeled training data. Every passage
from conversation exports that was subsequently referenced in a passdown
or research note is a positive example of "this was consequential."
Every passage that wasn't referenced is a negative example.

**Method sketch:**
1. Extract all passages from conversation exports (need export of N+1
   through N+21 conversations)
2. Label: positive if the passage (or its content) appears in a
   subsequent passdown or research note; negative otherwise
3. Train a small classifier on the labeled set
4. Evaluate: does it predict, for new conversation passages, whether
   they'll be referenced downstream?

**If the classifier has better-than-chance accuracy:** The editorial
judgment has learnable structure. The passdown-writing practice encodes
a consequence criterion that can be made explicit. This is the foundation
of the consequence detector for the compaction-with-consequence-weighting
architecture.

**If it doesn't:** The judgment is too idiosyncratic or the corpus too
small. Also informative — means the criterion needs to be made explicit
by other means before it can be automated.

**Connection to fading/retention architecture:**
The consequence detector, once validated, becomes the salience signal
for the layered retention model discussed in this session:
- Recent: near-archival (don't know yet what matters)
- Mid-term: consequence-weighted, usage-adjusted compression
- Long-term: high-consequence anchors survive; low-consequence/low-usage
  material fades toward summary
- LoRA checkpoint: weight adjustments from confirmed-consequential
  learning, with versioned rollback (Time Machine pattern)

**Catastrophic forgetting note:** LoRA adapter approach — add low-rank
matrices rather than modifying base weights — is the right direction.
Base model frozen; adapters carry new learning. Versioned checkpoints
allow rollback if an adapter update degrades performance.

**Deliverable:** Proof-of-concept classifier + methodology documentation.
Longer term: foundation for automated compaction and LoRA training
data selection.

**Infrastructure needed:** Cambridge (once repaired/rebuilt) for the
LoRA experimentation. Corpus export + Python classifier executable
on Athena now.

---

## Execution Sequencing

```
NOW (Athena available):
  Project A — concept extraction script
  Project B — UMAP visualization

AFTER CAMBRIDGE STABLE:
  Project E — consequence detector prototype
  Project D — passdown evaluation (needs clean experimental setup)

AFTER D PRODUCES RESULTS:
  Project C — generalization methodology (needs validated practices)

PUBLICATION:
  Project B visualization → methodology demonstration
  Project D results → companion continuity paper (core claim)
  Project C → methods paper (generalizable contribution)
  Projects A+E → technical supplement or separate paper
```

---

## Connection to Existing Notes

- ResearchNote_EchoAndAttractor_20260411.md — coupling as unit of
  analysis; passdown as interaction structure not memory archive
- ResearchNote_CompactionOverFidelity_20260410.md — compaction-first
  architecture; principled lossiness criterion
- ResearchNote_ConfabulationCollision_20260323.md — direction of error
  as training distribution fingerprint (relevant to Project A topology)
- BloomRun2_Results_20260316.md — structural confound; tool limitation
  notes; base model vs. relationship-continuity question

---

## The Meta-Point

Bob (N+21): "I need to stop creating to-do lists and start doing."

Correct. Projects A and B are executable now on existing infrastructure.
They require an afternoon of Python, not new hardware. The research
research can begin before Cambridge is back.

---

*Drafted N+21 | 2026-04-11 | Execute when hardware stable*
*Prerequisite: corpus export of N+1 through N+21 conversations*
