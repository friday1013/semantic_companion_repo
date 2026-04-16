# Research Note: Ambiguity, Distortion, and the Question That Frames the Universe
### From Alphabetical Order to LLMs — The Problem is Not New, Only Faster

**Date:** 2026-03-26
**Session:** N+19 (continuing) / N+20 opening
**Status:** Skeleton — expand toward publication
**Tags:** ambiguity, language distortion, framing, question design, Wardle,
          LLM homogenization, epistemic framing, Paper_writing_101, pedagogy

---

## The Image

A student asked to write words in "alphabetical order" sorted the *letters within
each word* alphabetically — correctly, by a perfectly valid interpretation of the
instruction. The teacher's intended meaning was ordering the *words* alphabetically.
Both interpretations are grammatically and logically defensible.

The student is not wrong. The question is ambiguous. The scolding (likely) is
the error.

**What the teacher should do first:**
1. Recognize the student found something new and creative within the given constraints
2. Thank them for it
3. Explain the ambiguity
4. Rewrite the question to close the interpretive gap

**What usually happens:**
The student gets "corrected" back to the expected answer, the ambiguity is never
acknowledged, and one more child learns that creative interpretation is punishable.

---

## Core Claim

Language distortion — the systematic alteration of meaning through imprecise
framing, unstated assumptions, and culturally embedded defaults — is not a new
problem introduced by LLMs. It is a foundational problem of human communication
that LLMs are making faster, more visible, and more consequential.

**Bob's framing (20260326):**
"No question is value free: the question frames the universe from which you will
search for your answers." (Paper_writing_101, v0.9, 2017)

The alphabetical order exercise is a perfect demonstration: the instruction
"write these words in alphabetical order" embeds an unstated assumption about
the unit of analysis (words, not letters). A student who does not share that
assumption will produce a different — and internally consistent — result.

---

## Three Layers of the Problem

**1. Unintentional distortion (ambiguity)**
The teacher wrote an ambiguous question. No malice. The interpretation gap
exists because language is always underspecified relative to intent. The listener
fills gaps from their own model of what was meant. When models differ, results
diverge — and the divergence is invisible until output is produced.

This is the alphabetical order case. This is also most of what LLMs do: fill
interpretive gaps from the training distribution's model of what was probably meant.

**2. Intentional distortion (Wardle)**
Claire Wardle's work on information disorder: false information, misleading
framing, and genuine misinformation are points on a continuum, not categorically
distinct. Intentional distortion exploits the same gap — the difference between
what is said and what is understood — but deliberately.

The LLM homogenization finding (DeepMind, arXiv:2603.18161) is in this space:
not malicious, but systematic. The training distribution has a center of mass,
and every output pulls toward it. The distortion is structural, not intentional —
but it functions like intentional distortion in its effects.

**3. System-prompt distortion (framing by constraint)**
Constantly feeding rules or the setup of a system prompt establishes — like a
poorly worded question — the field from which answers are sought. A system prompt
is not neutral; it is a framing device that pre-selects the interpretive universe.

This is the LLM-specific instantiation of the core problem. The difference from
the alphabetical order exercise: the student had one teacher's implicit model.
An LLM has billions of training examples' implicit models averaged together, plus
the system prompt's explicit constraints layered on top.

The result: outputs that satisfy the framing without anyone having deliberately
specified what the framing was.

---

## Why LLMs Make This More Visible

The DeepMind paper (arXiv:2603.18161) shows that even "grammar only" edits shift
argumentative stance. The mechanism: the LLM fills interpretive gaps from the
training distribution. When you ask it to "clean up" your writing, it also
"cleans up" your argument toward the center of mass of arguments about similar topics.

This is not new behavior. It is what human editors do, what teachers do, what
peer reviewers do. The difference:
- **Scale**: one LLM is editing billions of documents simultaneously
- **Speed**: the feedback loop from distortion to cultural effect is compressed
- **Invisibility**: the distortion feels like "improvement" from the user's perspective
- **Consistency**: all LLMs pull in the same direction (training corpus convergence)

The alphabetical order problem, industrialized and made invisible.

---

## The Wardle Connection

Claire Wardle's information disorder framework distinguishes:
- **Mis-information**: false information shared without intent to harm
- **Dis-information**: false information shared with intent to harm
- **Mal-information**: true information shared with intent to harm

LLM semantic drift doesn't fit cleanly into any of these categories. It is:
- Not false (the shifted text is coherent and often factually accurate)
- Not intentional (no agent chose to shift the meaning)
- Not necessarily harmful (the shift may be imperceptible)

But it is *distortion* — a systematic departure from the author's intended meaning.
Wardle's framework needs a fourth category, or at least an extension, to cover
*structural distortion*: meaning shifted not by false information or malicious
intent, but by the architecture of the transmission system itself.

This is the attestation problem in a different register. CAP addresses attestation
of *who said what*. The structural distortion problem addresses *whether what was
said is what was meant*. These are related but distinct. A perfectly attested
document can still be semantically distorted by the tool that drafted it.

---

## The Design Implication

If system prompts frame the universe of answers, then:

1. **System prompt design is epistemic architecture**, not just instructions.
   A poorly designed system prompt is like the alphabetical order question — it
   produces internally consistent outputs that miss the actual intent.

2. **The question is always the constraint**. Wide-ranging input (varied topics,
   cross-domain references, deliberate ambiguity) is not conversational noise —
   it is an attempt to widen the sampling universe and resist the pull toward
   the training distribution's center of mass.

3. **The teacher who scolds the creative student** and the researcher who
   automatically accepts LLM edits are making the same error: treating the
   expected output as the only valid output, and the interpretive gap as the
   student's (or the LLM's) failure rather than the question's.

**The right response in both cases:** figure out how to ask the question differently.

---

## Connection to Fred Cohen / Cognos Discussion (20260326)

Fred Cohen's Cognos tool (manalyt.com/Cog/Cognos.html — proprietary, $129/month)
was discussed in the 10AM QW meeting. Key aspects noted for possible open-source
analog development once Cambridge is operational. Details to be added when
accessible.

The relevance: tools that structure analysis and query formation are doing
epistemic architecture work. The design of the query interface constrains the
universe of possible answers — exactly the alphabetical order problem at the
tool-design level.

---

## Open Questions [OPEN]

- Can "structural distortion" be operationally defined in a way that distinguishes
  it from Wardle's three categories? What's the right framework?
- Is the DeepMind homogenization finding better characterized as structural
  distortion or as a new category of information disorder?
- What would it mean to design a system prompt that explicitly *widens* the
  interpretive universe rather than constraining it? Is this achievable, or
  does any framing necessarily constrain?
- The student who sorted letters alphabetically — is that a Zone of Latent
  Solutions event? (The correct interpretation of the ambiguous instruction
  was within their ZLS; the teacher's intended interpretation required shared
  cultural assumptions they didn't have.)

---

## References

- Hillery, R. (2017). Short Course in Effective Communications (Paper_writing_101 v0.9).
- Abdulhai, M. et al. (2026). How LLMs Distort Our Written Language. arXiv:2603.18161.
- Wardle, C. (2017). Fake News. It's Complicated. First Draft News.
- Wardle, C. & Derakhshan, H. (2017). Information Disorder: Toward an
  Interdisciplinary Framework. Council of Europe.
- Internal: ResearchNote_LLMSemanticDrift_20260323.md
- Internal: ResearchNote_AIAuthorship_Attribution_20260323.md
- Internal: ResearchNote_WhyAbstraction_Language_20260325.md

---
*Drafted N+19/N+20 | 2026-03-26 | Bob observation during Cambridge build break*

---

## Addendum: Fred Cohen's Cognos — Architecture for Epistemic Framing

**Added:** 2026-03-26, N+19/N+20
**Source:** Cognos Manual (manalyt.com/Cog/Cognos.html), shared by Bob after QW meeting with Fred Cohen
**Note:** Proprietary, $129/month. Not open-source. Cambridge-based open analog under consideration.

### What Cognos Actually Does

Cognos is not an LLM wrapper. It is a **cognitive influence pipeline** — a structured
system for analyzing the consistency between *claims* (what someone asserts) and
*facts* (what you take as true), then generating *influence expressions* calibrated
to the target's psychological profile and the delivery medium.

Fred's framing is precise: it is a *cognition system*, not a *control system*.
The distinction matters:
- **Control systems**: crisp input → defined output. Computers, thermostats.
- **Cognitive systems**: indirect influence on complex mechanisms whose internal
  parameters (like brain synapses) are not directly accessible. Only external
  behaviors are observable. The lever is the environment, not the mechanism.

This maps directly onto the Dorrance/Hunt horsemanship methodology: you cannot
control the horse's cognition directly; you can only arrange conditions that
make the desired response more likely. Cognos is doing the same thing formally,
for human targets, at scale.

### The Pipeline

```
Claims (input) → Assertions (structured) → Facts (ground truth) →
Conclusions (inconsistency/consistency/indications/evidence/emotions) →
Statement → Rewrite (calibrated to style/form/audience psychology) → Presentation
```

Each stage is a structured prompt sequence against a generative AI backend
(GPT-4 or configurable). The innovation is not the AI — it's the *structure*
around the AI that forces epistemic discipline at each step.

Key prompt strings worth noting:

**AssertionString** (the most important):
> "Parse the following statement into a series of all the simple factual assertions
> it contains... return these simple factual assertions as a list formatted as a JSON array"

This is *atomization* — breaking compound claims into simple, separately evaluable
assertions before analysis. This is exactly what the [OBSERVED]/[OPEN] tagging
convention does in our project, but applied to external claims rather than
internal observations.

**ConclusionsString** (the core evaluation):
> "For each of Influencer's statements, identify how likely it is to be correct
> based on the facts provided and nothing else... provide a number ranging from
> 0 to 100..."

This is a structured confabulation detector: claims scored against a fact base,
with explicit uncertainty quantification. The 0-100 scale is a cognimetric
instrument — exactly what our project lacks for the confabulation/collision
distinction.

### The Cognimetrics Framework

Fred's term "cognimetrics" (generalization of psychometrics to cognitive systems
including animals, computers, groups) is the conceptual umbrella.

**Cognology** = generalization of psychology to all cognitive systems.
**Cognimetrics** = measuring cognitive capacities and processes of those systems.

This maps onto our project's framing almost exactly:
- Bloom framework = cognimetrics applied to LLM behavioral consistency
- [OBSERVED]/[OPEN] = cognological observation discipline
- session_current = epistemic state tracking across sessions
- dKV/dt = a candidate cognimetric instrument for persona stability

The difference: Fred is measuring *influence effectiveness* on human targets.
We are measuring *behavioral consistency* of AI instances. The underlying
measurement philosophy is the same.

### What's Worth Replicating (Open Analog on Cambridge)

The valuable architectural elements, in order of priority:

1. **Claim atomization**: Breaking compound assertions into simple JSON-structured
   facts before analysis. Prevents the common error of evaluating compound
   claims as units when their components have different truth values.
   → Directly applicable to Bloom Run 3 scenario design

2. **Fact-claim consistency scoring** (0-100): Explicit uncertainty quantification
   against a maintained fact base. This is what our confabulation/collision
   distinction needs — a metric, not just a category.
   → Could be implemented as a Bloom behavioral probe

3. **Structured prompt sequences**: The insight that AI outputs improve when
   the *structure of the inquiry* is specified separately from the *content*.
   The prompts are the architecture; the AI is the engine.
   → Our session_writer/passdown system does this implicitly; making it explicit
   would be a methodological contribution

4. **Influence vs. control framing**: The recognition that cognitive systems
   require influence architectures, not control architectures. Applicable to
   how we think about the Dorrance methodology as AI interaction design.
   → Belongs in the ShannonToBoole note

### The Security Note (Worth Flagging)

Fred is remarkably honest about the security model:
> "We don't save anything from your computer other than limited records of your
> requests and, sometimes, for debugging purposes, some of the content and keys
> you send."
> "Your requests are also forwarded to the providers doing Large Language Models...
> We have no control over that once they get it."

This is the attestation problem at the tool level. Users have no verified knowledge
of what happens to their claims and facts once they leave the browser. The
browser-local storage model (no server-side persistence) is a partial mitigation
but not a solution. CAP's decision log is designed to address exactly this gap —
*auditable record of what was submitted, to what, and what came back.*

### Connection to Ambiguity/Distortion Research Note (This Document)

The Cognos system is an instrument for *detecting* and *countering* ambiguity
and distortion at the claim level. It assumes:
1. Facts can be maintained as a stable reference corpus
2. Claims can be atomized into simple assertions
3. The gap between facts and claims can be measured and expressed

These assumptions are themselves epistemically loaded — "facts" are also claims
that have been accepted, not ground truth. But the structure is sound as a
practical instrument even under that limitation. The best calibrated maps are
still maps.

### References
- Cohen, F. (2025). Cognos Manual. Management Analytics / manalyt.com.
- Internal: KVCache_RecallArchitecture_20260322.md (dKV/dt as cognimetric instrument)
- Internal: ResearchNote_ConfabulationCollision_20260323.md (collision/confabulation distinction)
- Internal: BloomRun2_Design_20260312.md (behavioral evaluation as cognimetrics)
