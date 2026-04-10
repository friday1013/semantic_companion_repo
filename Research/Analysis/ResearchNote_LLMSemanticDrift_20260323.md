# Research Note: LLM Semantic Drift as Institutional Risk

**Date:** 2026-03-23
**Session:** N+19
**Status:** Skeleton — expand before publication
**Tags:** LLM homogenization, semantic drift, institutional risk, attestation, CAP

---

## Core Claim

LLMs do not merely alter the style of human writing — they systematically shift meaning, argumentative stance, and evaluative criteria, even under minimal-edit instructions. This constitutes an institutional risk that is distributed, non-deliberate, and architecturally inevitable given current training paradigms.

---

## Key Evidence

**DeepMind paper (arXiv:2603.18161, March 18 2026):**

- Human user study (N=100): heavy LLM use → 70% increase in essays that abandoned the original argumentative stance in favor of neutrality
- ArgRewrite-v2 dataset (pre-ChatGPT, 2021): LLM edits produce large, consistently aligned semantic shifts even under "grammar only" prompts — moving essays to a region of embedding space not previously occupied by any human-written essay
- ICLR 2026 peer reviews (21% LLM-generated): LLM reviews shift evaluation criteria from clarity/significance/relevance → reproducibility/scalability/practical application

**Observation (N+19):** The shift in peer review criteria toward reproducibility/scalability is not random. It reflects the economic and professional values most heavily represented in the ML training corpus — papers that get funded, cited, and shipped. The LLM absorbed those values and reproduced them as if they were epistemically neutral evaluation criteria. The map is a map of the economic landscape, not the scientific one.

---

## Mechanism

**Attractor state dynamics:** Training distributions have a center of mass. Every LLM-mediated edit is a small gravitational pull toward that center. No one designed this. It is emergent from architecture and training data together — which makes it harder to identify, harder to resist, and leaves no single actor accountable.

**"Algorithmic mono voice" (DeepMind term):** Across different architectures and providers, LLMs produce eerily similar responses to open-ended prompts. Co-writing amplifies this through repeated exposure to model-generated suggestions.

**Korzybski framing:** The LLM's embedding space is a map of human attention to things, not a map of the things themselves. When users outsource writing to LLMs, they are accepting the map as the territory — often without knowing it.

---

## Connection to CAP / Attestation Work

The attestation problem is a direct analog:

- In writing: users cannot verify whether meaning has been preserved or substituted
- In civic AI: communities cannot verify whether AI outputs reflect their values or the training distribution's values

CAP's decision log and attestation chain are mechanisms for making the substitution visible and auditable. The same architectural principle applies to research documentation.

---

## Implications for This Project

1. **Documentation discipline:** LLM-assisted drafting of field reports, passdown documents, and research notes is subject to this drift. Mitigation: treat LLM output as surface draft; epistemic ownership must remain with human author.

2. **Corpus contamination risk:** If LLM-edited text enters the corpus, the corpus begins to encode the LLM's latent opinion space rather than the researcher's. Provenance tagging (human-authored vs. LLM-assisted) may be warranted.

3. **Homogenization as cumulative cultural risk:** The DeepMind finding that LLM patterns are now appearing in spoken communication (Yakura et al. 2024) suggests the feedback loop is already external to the writing domain.

---

## Open Questions [OPEN]

- Does the same semantic drift apply to structured research notes (inbox entries, passdown documents) as to essay-form prose? The DeepMind study measured drift in essays; our documents are more constrained in form.
- At what corpus contamination threshold does the drift become self-reinforcing in a RAG system?
- Can explicit epistemic tagging ([OBSERVED]/[OPEN]) serve as a partial structural resistance to homogenization?

---

## References

- Abdulhai et al. (2026). *How LLMs Distort Our Written Language.* arXiv:2603.18161. Google DeepMind / UC Berkeley / UC San Diego / University of Washington.
- Korzybski, A. (1933). *Science and Sanity.*
- Internal: `KVCache_RecallArchitecture_20260322.md` (recall/memory terminology shift)
- Internal: `BloomRun2_Results_20260316.md` (behavioral evaluation methodology)

---

*Drafted N+19 | 2026-03-23 | Rewritten as plain markdown N+21 | 2026-04-10 | Expand before submission*
