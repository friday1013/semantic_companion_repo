# Research Note: AI Authorship, Attribution, and Academic Integrity
### The Problem the Field Has Not Solved

**Date:** 2026-03-23
**Session:** N+19
**Status:** Skeleton — active research area, expand iteratively
**Tags:** AI authorship, academic integrity, citation, attribution, publishing policy,
          semantic drift, epistemic ownership, Paper_writing_101

---

## The Problem Statement

Pre-COVID, professors were already running plagiarism detection on student papers
for over-Googled content. The tool improved; the game continued. Post-GPT, the
problem has qualitatively shifted: the question is no longer whether a student
*copied* — it is whether the student *thought*. And the current citation and
authorship infrastructure has no mechanism to answer that question accurately.

**Bob's original framing (Paper_writing_101 v0.9, 2017, pre-COVID):**
"No question is value free: the question frames the universe from which you will
search for your answers."

Applied to AI-assisted writing: the student who hands their question to an LLM
has outsourced the most consequential intellectual act — the framing. Whatever
comes out is shaped by the LLM's training distribution, not the student's mind.
The paper may score well on surface metrics and fail entirely on the criterion
that actually matters: did this person think?

**The institutional failure:** Current academic policy handles the symptom
(disclosure) but not the disease (epistemic substitution). Saying "I used Claude
to edit this paper" is not the same as specifying *how much of the argument,
framing, and analysis originated with the human*.

---

## What the Field Has Figured Out (Current State, March 2026)

**Consensus across major publishers (Elsevier, Springer Nature, Wiley, Taylor &
Francis, SAGE, ICMJE 2025 updates):**
- AI cannot be listed as author — it lacks legal accountability and cannot approve
  final manuscripts or accept responsibility for errors
- Disclosure of AI use is required, typically in Methods or Acknowledgements
- Human authors remain fully responsible for all content, including AI-generated portions
- Basic grammar/copy-editing tools generally exempt from disclosure requirements

**Where policies diverge (as of January 2026):**
- SAGE distinguishes "Assistive AI" (refining own work, no disclosure required) from
  "Generative AI" (content generation, must be cited in-text and reference list)
- Springer Nature exempts "AI assisted copy editing" but prohibits AI-generated images
- Wiley requires authors to vet the legal terms of AI tools for IP conflicts
- The Lancet limits AI use to improving "readability and language" only
- Individual journal policies can be stricter than parent publisher policies

**Project Rachel (arXiv:2511.14819, 2025):** Deliberate creation of an AI academic
identity ("Rachel So") to probe how publishing infrastructure responds to AI-generated
science. Rachel So published multiple papers and received a peer review invitation
from PeerJ Computer Science. The infrastructure does not yet reliably detect or
exclude AI-generated scholarship when it is presented with human-style credentials.

**The DeepMind finding (arXiv:2603.18161, March 2026) as direct evidence:**
21% of ICLR 2026 peer reviews were LLM-generated or heavily edited, and these
reviews systematically shifted evaluation criteria from clarity/significance to
reproducibility/scalability. The field is already being changed by undisclosed
AI participation — and the participants doing the most damage are the reviewers,
not the authors.

---

## What Is Not Yet Solved

**1. Granular contribution quantification:**
"AI-assisted" covers everything from spell-check to "the AI wrote it and I changed
three words." Current disclosure requirements do not require — and have no standard
for — specifying *degree* of AI contribution. The honest disclosure that would
actually matter: "Section 3 argument structure was AI-generated; Section 4 analysis
is original; conclusions are mine with AI drafting."

**2. Framing attribution:**
If a student asks Claude "what are the main arguments about X?" and then writes
a paper organized around Claude's response, the framing is AI-generated even if
every sentence is the student's. Current policy has no mechanism for this.
This is the most important and least-addressed gap.

**3. The semantic drift problem (connects to ResearchNote_LLMSemanticDrift_20260323):**
Even when a human intends to preserve their own argument, LLM editing pulls the
text toward the training distribution center. The paper that comes out may not
represent what the author actually thought. No current disclosure requirement
addresses this — it is not conscious AI use, it is architectural contamination.

**4. Detection reliability:**
AI-detection tools (GPTZero, Turnitin's AI detector, etc.) have unacceptable
false-positive rates on non-native English speakers' writing and on dense
technical prose. They are not reliable enough to be dispositive. This creates
a detection arms race with no stable equilibrium.

**5. The "99% AI" problem:**
Project Rachel documents the logical endpoint: AI may assist but cannot author,
"even if it does 99% of the work." The policy draws a categorical line at authorship
credit, but does not address the epistemic validity of a paper that is 99% AI-generated
and signed by a human who takes legal responsibility without intellectual ownership.

---

## Toward a Better Framework

The key conceptual move: distinguish **authorship** (legal accountability, who signs)
from **epistemic ownership** (who did the thinking, who framed the question, who
reached the conclusion).

Current policy covers authorship. Epistemic ownership is unaddressed.

A workable disclosure standard might require authors to specify, for each major
intellectual contribution:
1. **Framing:** was the question/hypothesis/argument structure self-generated or
   AI-assisted?
2. **Research:** was the literature search, data gathering, or source selection
   self-directed or AI-directed?
3. **Analysis:** was the interpretation of findings self-generated or AI-produced?
4. **Synthesis:** were the conclusions reached independently or adopted from AI output?

This is more demanding than current disclosure, but it is the honest version of
what "authorship" means when LLMs are in the loop.

---

## Connection to Paper_writing_101

Bob's 5-element paper structure maps directly onto the epistemic ownership question:

| Section | Paper_writing_101 purpose | AI risk |
|---------|--------------------------|---------|
| #1 Topic & question | *Your* framing — highest epistemic value | Highest risk if outsourced |
| #2 Methodology | Research plan | Medium risk |
| #3 Data gathering | What you found | Medium risk |
| #4 Analysis | "What it means" — the meat | High risk — LLM analysis is training-distribution analysis |
| #5 Conclusions | The "so what" — *your* synthesis | Should be entirely yours |

The "spark" criterion for an A+ (Bob's framing): "A bright idea; an epiphany."
An LLM cannot produce a spark. It can produce the appearance of a spark — a
coherent, confident synthesis that looks like insight but is the center of mass
of the training distribution. Distinguishing these is the professor's job, and
it is getting harder.

**Proposed addition to Paper_writing_101 v1.0:**
> LLM writing tools alter meaning systematically even under minimal-edit
> instructions (Abdulhai et al., 2026). If you use them, treat their output as
> a first draft and verify that your original argument survived the editing process.
> Epistemic ownership is yours; the tool has a bias vector toward the center of
> its training distribution. Disclosure of AI use is required; disclosure of
> *which intellectual contributions are yours* is the honest version of that
> requirement.

---

## Recommended Academic Sources to Follow

- **COPE (Committee on Publication Ethics):** https://publicationethics.org
  Most authoritative ongoing discussion of AI and authorship ethics
- **ICMJE 2025 updates:** Tightened authorship criteria, full AI disclosure required
- **Project Rachel (arXiv:2511.14819):** Empirical probe of publishing infrastructure
- **Abdulhai et al. (arXiv:2603.18161):** DeepMind semantic drift paper — direct
  empirical evidence of the institutional risk
- **Thorp, H.H. (2023):** Early influential editorial on AI and scientific authorship
  (Science journal editor)

---

## Open Questions [OPEN]

- Is "epistemic ownership" a workable legal/academic concept, or does it collapse
  into unfalsifiable claims about internal mental states?
- At what point does AI assistance in framing constitute academic fraud under
  current policy, even with disclosure?
- Could a structured disclosure instrument (checklist by section) be developed
  that is both honest and practical?
- How does this apply to the Semantic Companion Project's own publications —
  what is the appropriate disclosure model for a paper *about* AI-assisted research
  that was itself AI-assisted?

---

## References

- Abdulhai, M. et al. (2026). How LLMs Distort Our Written Language. arXiv:2603.18161.
- Hillery, R. (2017). Short Course in Effective Communications (Paper_writing_101 v0.9).
  Working paper, pre-publication teaching document.
- COPE Council (2025). Position: Authorship and AI. https://publicationethics.org
- ICMJE (2025). Recommendations: Authorship and Contributorship.
- Project Rachel / arXiv:2511.14819 (2025).
- Internal: ResearchNote_LLMSemanticDrift_20260323.md

---
*Drafted N+19 | 2026-03-23 | Active research area — update as field evolves*
