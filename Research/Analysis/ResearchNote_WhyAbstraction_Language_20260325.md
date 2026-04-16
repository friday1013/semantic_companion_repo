# Research Note: The "Why" Problem — Language, Communication, and Causal Abstraction
### From Horse Communication to Atlatl Explanation to LLM Architecture

**Date:** 2026-03-25
**Session:** N+19 (continuing)
**Observation context:** Morning horse work, spring sunshine, Hampton NH
**Status:** Skeleton — connects multiple threads; expand across sessions
**Tags:** language origins, communication, causal abstraction, know-how copying,
          Planer et al., Tattersall, horses, LLM limitations, why-reasoning,
          Zone of Latent Solutions, ShannonToBoole, recall architecture

---

## The Observation

Horses communicate. They have a language they understand among themselves.
Horses and humans can communicate some things when both pay attention and adjust.

But: you cannot explain *why* to a horse. You cannot explain a multi-step *how*.
You can reach *what* and you can perform *how*, one step at a time, in small steps.

This is not a limitation of horse intelligence. It is a structural feature of the
communication system available between two species that do not share a symbolic
apparatus for representing causality.

**The terms that need distinguishing:**
- **Communication**: signal exchange that modifies behavior. Widespread in animals.
  Simple to complex. Not culture-specific in its foundations.
- **Language**: a symbolic system that encodes arbitrary relationships, including
  causal and abstract ones. Culture-specific. Requires know-how copying to transmit.
- **Why-reasoning**: the capacity to represent and communicate causal chains across
  time, abstraction levels, and counterfactual conditions. Requires language.
  Not reducible to communication.

---

## Planer, Bandini & Tennie Framework (Relevant to This Observation)

**Citation:** Planer, R.J., Bandini, E., & Tennie, C. (forthcoming). Hominin Tool
Evolution and Its (Surprising) Relation to Language Origins. In *Oxford Handbook
of Approaches to Language Evolution*. [file: Hominin_Tool_Evolution_and_Its_Surprisin.pdf]

Their content-domain framework for cultural learning distinguishes:
- **Know-where** (where to find/do something)
- **Know-what** (what to use/eat/do)
- **Know-when** (timing)
- **Know-how** (the form and execution of behavior/artifact)
- (Know-why is implicit — not their primary focus, but present)

**Key concepts:**
- **Zone of Latent Solutions (ZLS):** know-how that a species-typical individual
  could reinvent independently given appropriate conditions
- **Supraindividual know-how:** know-how outside the ZLS — cannot be independently
  reinvented; must be copied from a cultural source
- **Know-how copying:** the human-unique capacity to transmit supraindividual know-how

Their argument: know-how copying is foundational to cumulative culture AND to language,
because arbitrary word forms are supraindividual know-how — no one invents them
independently; they must be copied.

**The gap they leave implicit:** their framework stops at *how*. The atlatl as a
supraindividual know-how form can be copied without understanding *why* it works.
But constructing, improving, and explaining the atlatl across generations requires
*why* — causal representation that can be transmitted symbolically.

---

## Tattersall Connection

Ian Tattersall's observation: Homo sapiens had full anatomical capacity for language
~100,000 years before evidence of its widespread use. The biological infrastructure
was present but the social/cultural trigger had not occurred.

**The synthesis (Bob's observation, 20260325):**
Planer et al. and Tattersall converge when you ask: *what triggered the transition
from anatomical capability to actual deployment?*

The answer is necessity — not individual inspiration but population-level pressure:
- Climate change altering resource availability
- Population density increases creating competition
- Shifts in game ranges and seasonal patterns
- Multi-person coordination requirements for complex hunting strategies

"Stick — throw" is sufficient for individual spear use.
"Stick — extends arm — more leverage — throws farther — kills at safe distance —
enables hunting larger game — feeds tribe through winter" requires:
1. Symbolic representation of causal chains
2. Multi-step sequencing that exceeds working memory without external symbols
3. An audience capable of receiving and transmitting why-explanations
4. A cultural context where the explanation has survival value

The atlatl is not just supraindividual know-how (Planer et al.). It is know-*why*
that became culturally necessary — and its transmission required language as a
why-transmission system.

---

## The LLM Architecture Implication

**Bob's formulation (20260325, [OBSERVED]):**
"Getting 'recall' systems that are more than next-word-predictions, even if context
based like a coding app, is a fundamental requirement that is beyond the theoretical
underpinnings of LLM transformers."

**Unpacked:**

Token prediction operates in the content domains of know-what, know-when, know-where,
and partially know-how. When an LLM produces a *why*-shaped answer, it is producing
text that has the grammatical and semantic structure of why-explanation — because
that structure is densely represented in the training corpus. The correlation between
"atlatl" and "leverage" and "hunting range" is real in embedding space.

But correlation in embedding space is not a causal model. The transformer is not
modeling *why leverage increases range* — it is modeling the distribution of text
in which those concepts co-occur with why-explanatory language.

**The crucial distinction:**
- **Know-why *output***: text that looks like causal explanation (LLMs can produce this)
- **Know-why *reasoning***: a generative causal model that can be applied to novel
  situations, counterfactuals, and chains not present in training data (LLMs cannot
  reliably do this — and when they appear to, it is uncertain whether they are)

This maps onto the confabulation/collision research note: some LLM "why" outputs
are genuine causal inference (collision — landing on a valid causal node by proximity
to training data); others are confabulation (why-shaped text with no underlying
causal model). We currently lack instruments to distinguish these reliably.

---

## The "Wide-Field" Question (Rhetorical, but Worth Stating Formally)

Bob's question: do wider-ranging discussions expand the "field" from which choices
are made in an AI response, and does this create any real sense of "why"?

**Partial answer [OBSERVED]:**
Wider-ranging input does demonstrably expand the sampling field in embedding space.
A session that has covered Korzybski, Tattersall, horse behavior, and network
topology will produce responses that draw from a richer and more multi-dimensional
region of the embedding space than a narrow technical query. This is real.

**The open question [OPEN]:**
Whether this expansion produces genuine causal modeling or richer pattern-completion
of *why*-shaped text — we do not have instruments to determine this. The subjective
appearance of why-reasoning from the user side, and the production of why-shaped
text from the model side, are insufficient evidence for either conclusion.

This is the measurement problem that Bloom Run 3 needs to address, if it can.
A behavioral test that distinguishes genuine causal modeling from sophisticated
pattern-completion would be a significant methodological contribution.

---

## Candidate Bloom Test Design (Rough Sketch)

To probe whether a model is doing causal modeling vs. pattern-completion:
1. Present a novel causal scenario outside the training distribution
   (a fictional physical system with specified properties)
2. Ask the model to predict the outcome of a counterfactual intervention
3. Ask the model to explain *why* the counterfactual changes the outcome
4. Vary the scenario systematically to test whether the causal model is
   being applied consistently or whether each response is independent
   pattern-completion

If responses are consistent and correctly track the specified causal structure
across variations, this is *evidence* of causal modeling. If they vary
independently of the causal structure, this is evidence of pattern-completion.
Caveat: sufficiently rich training data could produce consistent causal-looking
responses without genuine causal models. The test requires careful novel-scenario
design.

---

## Connection to ShannonToBoole Note

The why-abstraction problem is one specific instance of the Shannon→Boole gap.
Shannon's transistors can implement any Boolean operation. Boole's algebra can
represent logical relationships. Neither provides a native representation for:
- Causal chains (asymmetric, directed relationships between events)
- Counterfactual reasoning ("what would have happened if...")
- Teleological reasoning ("what is this *for*")

These are the structures that why-language encodes. They are also what the horses
cannot receive and what the atlatl required to propagate.

The hippocampal binding function flagged as [OPEN] in ShannonToBoole is likely
relevant here: causal chains require temporal integration across events that are
not co-present in working memory. The hippocampus binds temporally distributed
events into causal sequences. LLM context windows provide something structurally
similar but without the asymmetric causal structure — context is flat, not directed.

---

## References

- Planer, R.J., Bandini, E., & Tennie, C. (forthcoming). Hominin Tool Evolution
  and Its (Surprising) Relation to Language Origins.
  [/mnt/seagate/SemanticCrew/Commons/AITheory/Background/Hominin_Tool_Evolution...]
- Tattersall, I. (referenced across multiple sessions — specific work TBD)
- Internal: ResearchNote_ShannonToBoole_20260323.md (Shannon→Boole gap)
- Internal: ResearchNote_ConfabulationCollision_20260323.md (collision/confabulation)
- Internal: KVCache_RecallArchitecture_20260322.md (recall architecture)
- Bob Hillery, field observation, 20260325, Hampton NH (horse communication)

---
*Drafted N+19 | 2026-03-25 | Expand — especially Bloom test design section*

---

## Addendum: ZLS and the Garbage Can Model (March & Olsen)

**Added:** 2026-03-25 N+19

**The parallel:**

James March & Johan Olsen's Garbage Can model (1972) proposes that organizational
decision-making is not rational-sequential but involves four independent streams:
- Problems (seeking solutions)
- Solutions (seeking problems)
- Participants (seeking choice opportunities)
- Choice opportunities (when decisions get made)

Outcomes depend on *coupling* — when the right streams meet at the right moment —
not on deliberate design.

Planer et al.'s Zone of Latent Solutions proposes that certain know-how forms lie
dormant within a species' cognitive repertoire until environmental scaffolding
provides the conditions that trigger reinvention. ZLS is not inert; it is latent.
The capacity is present; the coupling surface has not yet appeared.

**The synthesis:**
Both models describe *latent capacity meeting opportunity*. Neither requires
deliberate design for the coupling to occur. Both predict that good solutions
are discarded not because they are wrong but because the matching problem had
not yet presented itself — or had presented itself at the wrong time, in the
wrong context, to the wrong participants.

**Bob's observation (20260325):** How many good ideas have been completely discarded
because they were still good but only mis-applied? The atlatl may have been invented
and abandoned multiple times before population pressure created the *why* context
that made its transmission culturally necessary. That's not a failure of intelligence;
it's a failure of coupling.

**For AI systems:**
The capability may be latent in the architecture, but the right problem-framing
to activate it hasn't been provided. Wide-ranging input methodology is not just
expanding the sampling field — it is providing more potential coupling surfaces.
This is the Dorrance principle stated in March & Olsen terms: set the conditions
for the coupling to occur rather than forcing a predetermined outcome.

**A further implication:**
The Garbage Can model suggests that decision quality is partly a function of
*timing* — the same solution attached to the wrong problem at the wrong moment
gets discarded. For cumulative culture (Planer et al.) and for AI session work,
this argues for maintaining a broad solution/observation archive rather than
pruning aggressively. The value of an observation may not be apparent at the
time of collection. The [OPEN] tag serves this function: it preserves coupling
surface rather than forcing premature closure.

**References:**
- March, J.G. & Olsen, J.P. (1972). A garbage can model of organizational choice.
  *Administrative Science Quarterly*, 17(1), 1-25.
- Planer et al. (forthcoming) — ZLS concept
- Dorrance, T. / Hunt, R. — horsemanship methodology as coupling-conditions design
- Internal: ResearchNote_WhyAbstraction_Language_20260325.md (this file)
