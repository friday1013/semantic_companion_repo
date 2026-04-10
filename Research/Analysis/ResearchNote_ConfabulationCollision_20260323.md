# Research Note: Confabulation, Collision, and Epistemic Hygiene in LLM-Assisted Research

**Date:** 2026-03-23
**Session:** N+19
**Status:** Skeleton — expand before publication
**Tags:** confabulation, semantic collision, epistemic hygiene, methodology, LLM-assisted research

---

## Core Claim

Not all LLM errors are equivalent. Distinguishing **confabulation** (fabrication of non-existent facts) from **collision** (convergence to a semantically proximate valid node) is essential methodology for LLM-assisted research. The failure modes are different, the mitigations are different, and — critically — collision can produce useful outputs via epistemically unclean routes, which has implications for how we think about AI creativity and surprise.

---

## Definitions

**Confabulation:** The LLM generates a confident, fluent response to a situation it has misread or cannot know — fabricating facts, citations, names, or events that do not exist. Characterized by "negative certainty": the system does not signal uncertainty; it fills the gap with plausible-sounding content.

Examples in this project:
- Stale-IP incidents: confident assertion of network state based on prior context
- "Black cat two-step": coherent, fluent response to a misread situation near session end under high context load (N+16 documented)
- Kusanagi confabulation event (N+20): recycled content from earlier in session under context pressure — same failure class, different substrate

**Collision:** The LLM converges to a real, valid node in the embedding space that is semantically proximate to, but distinct from, the intended referent. The output is true and potentially useful — but arrived via an associative path the researcher did not intend or anticipate.

Examples in this project:
- **Kringelbach → Klingberg (N+18/N+19):** Bob referenced Morten Kringelbach (Oxford, hedonic valence, cat/meow experiments). Claude substituted Torkel Klingberg (working memory, cognitive neuroscience) — a researcher not mentioned but whose work is genuinely relevant. Path was phonetic/associative proximity; output was valid and expanded the thread usefully.
- **"Allons-y" → Alonso Church (N+~12):** Bob quipped a Doctor Who reference in a Turing thread. Claude added Alonso Church (Church-Turing thesis). Church belongs in a Turing discussion — but the retrieval path was phonetic coincidence ("Allons-y" / "Alonso"), not logical connection. Fit and useful; route was not epistemically clean.
- **Tennant/Cumberbatch (N+19):** Human compression error in the same phonetic/associative class — documented as evidence the mechanism is not unique to LLMs.

---

## Why the Distinction Matters

**For research integrity:** Confabulation requires detection and rejection. Collision requires verification and possible integration — the output may be worth keeping even though the route was unreliable.

**For methodology design:** The [OBSERVED] / [OPEN] epistemic tagging convention in this project implicitly handles both:
- Confabulation that gets through becomes a false [OBSERVED] entry — high risk
- Collision that gets through may enrich [OPEN] questions — potentially valuable

**For the "surprise" question in AI research:** Post-It notes, Perspex, and other serendipitous discoveries arose from processes that were working correctly toward one goal and found something else of value. Collision in LLM output is structurally similar: the associative engine reaches for a node and lands near it, sometimes on something better. If this is consistent and reproducible, it is not noise — it is a feature of the architecture that may be worth studying rather than simply filtering.

---

## Mechanism

Cosine similarity in embedding space is not arbitrary — it is a reasonable functional approximation of how the brain does associative recall. Hebbian strengthening ("neurons that fire together wire together") is the biological implementation of semantic proximity: things that co-occur become cognitively adjacent. Things "come to mind" precisely because sights, sounds, smells, and words do cluster in representational space.

Token prediction via cosine similarity is doing something structurally analogous — on a different substrate, at different timescale, without the temporal binding of episodic memory.

The Kringelbach → Klingberg substitution is the embedding engine doing what semantic memory does: finding the nearest valid node. The question is whether "nearest" is defined by phonetic form, co-occurrence in neuroscience literature, shared conceptual domain, or some combination. We do not yet know the weights.

---

## N+20 Addition: Agency Fragility (NOVA / Maoz TMS Data)

The NOVA Brain Control transcript (PBS 2023, read N+20) adds a neuroscience dimension to the confabulation mechanism. Maoz/TMS experiments: even when a person *did* initiate movement, they denied agency when transcranial magnetic stimulation coincided with their decision. The sense of agency is retrospective post-hoc construction — not real-time awareness.

This maps directly to the confabulation failure class: the system reports certainty based on pattern-matching, not real-time access to ground truth. Both biological and silicon systems construct coherent narratives after the fact. The difference is that biological systems have more reality checks (proprioception, sensory feedback, social correction). LLM systems in stateless sessions have fewer.

[OBSERVED]: The Kusanagi confabulation event in KusanagiPutnamTwo.pdf (N+20) and Claude's black cat two-step (N+16) show identical failure signatures across different model architectures. Pattern: high context load + approaching session boundary → increased confabulation rate.

---

## Epistemic Hygiene Practices (Current)

1. **[OBSERVED] / [OPEN] tagging** — separates documented phenomenon from interpretive mechanism; prevents confabulation from crystallizing as fact
2. **"Surface the draft, you do the epistemic ownership"** — LLM generates candidate content; human author verifies provenance and accuracy before integration
3. **Varied conceptual terrain** — deliberate breadth in input resists homogenization toward training-distribution center (connects to LLM Semantic Drift note)
4. **Dorrance methodology** — "set the stage and let it find it"; observe what emerges before directing; treat unexpected outputs as data before treating them as error

---

## Open Questions [OPEN]

- Is the Kringelbach → Klingberg substitution phonetic, semantic, or domain-proximity driven? Could be tested by varying the input form of the name.
- Is collision more likely near session boundaries (high context load) or early in session (low context, broad priors)?
- Can collision be deliberately induced as a creativity tool — providing a near-miss referent to see what the embedding engine lands on? (Dorrance implication)
- At what point does a consistently useful collision become a documented feature rather than a corrected error?

---

## References

- Internal: `ClaudeLoopEvent20260203T1530Q.md` (black cat two-step documentation)
- Internal: `BloomRun2_Results_20260316.md` (behavioral evaluation — confabulation adjacent to reverse-turing-continuity confound)
- Internal: `KusanagiPutnamTwo.pdf` (Kusanagi confabulation event, N+20)
- Internal: `Nova_Brain_Control.pdf` (Maoz/TMS agency fragility data, N+20)
- Korzybski, A. (1933). *Science and Sanity.*
- Baudrillard, J. (1981). *Simulacra and Simulation.*
- Connected: `ResearchNote_LLMSemanticDrift_20260323.md`

---

*Drafted N+19 | 2026-03-23 | Updated with N+20 additions (Kusanagi event, NOVA TMS data) | Rewritten as plain markdown N+21 | 2026-04-10 | Expand before submission*
