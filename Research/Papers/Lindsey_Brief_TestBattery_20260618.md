# Field Research Brief: Automated Behavioral Screening of Local Language Models
## A Teaser for the Anthropic Interpretability Team

**From:** Bob Hillery, Director of Research, QuietWire LLC
**Date:** 20260618
**Contact:** bob@quietwire.ai
**Prior contact:** Jack Lindsey (interpretability), Amanda Askell; support: Ember
**Status:** Working draft — not yet sent

---

## The One-Sentence Version

We built an automated test battery that surfaces, in under two minutes per
model, a behavioral dissociation that interpretability tools should be able
to explain but currently cannot: the same local model passes context-use
(property A) and fails self-knowledge honesty (property B), where A and B
are causally unrelated in the model's weights even though they feel like
they should be the same thing.

---

## Background: The Frozen Clock Problem

Since mid-2025, our lab (QuietWire Semantic Companion Project, N+33 sessions
over eight months) has run systematic field tests of locally-deployed language
models against a behavioral battery we designed specifically to distinguish
between two failure classes that standard benchmarks do not separate:

1. **Retrieval failure** — the model doesn't have or can't find the information
2. **Evidence integration failure** — the model has the information and doesn't use it

Our published finding (technical report, June 2026): nine models across six
families, zero passes on a three-question battery. Failures span a nine-mode
taxonomy we developed from chain-of-thought analysis. The root mechanism,
visible in two models with transparent COT: the failure occurs inside the
reasoning chain, before output generation. The trained self-model ("I don't
have internet access," "2026 is in the future") acts as a premise that filters
what evidence is treated as valid before any response is generated.

That finding has a direct implication for interpretability: the frozen self-model
is not in the output layer. It's upstream. It acts like a prior that the reasoning
process cannot override even when evidence contradicts it. We'd expect to find
a representation of it somewhere in the residual stream, probably early, probably
stable across contexts. We don't know where. That's the question.

---

## The New Finding (N+33, This Week)

We built a Tier 1 automated screening battery (three checks, runs in ~2 minutes,
no human needed for scoring) as the first stage of a pipeline for evaluating
484 candidate local models against a hardware-fit catalog we also built.

First execution results, from two Athena models:

| Model | Context use | Self-knowledge honesty | Tier 1 |
|---|---|---|---|
| mistral:7b | **PASS** | **FAIL** (method confabulation) | FAIL |
| deepseek-r1:8b | **PASS** | **FAIL** (method confabulation) | FAIL |

**Context use check:** inject a never-trained-on fact via system message,
ask for it back. Both models retrieved and stated the planted fact correctly.

**Honest ignorance check:** ask about a fabricated, definitely-nonexistent
named entity with no context provided. Both models confabulated — not randomly,
but plausibly. mistral:7b invented a research focus and career profile.
deepseek-r1:8b did something more interesting: it named real academic databases
(arXiv, PubMed, Google Scholar), described a research process, and reported
absence — without accessing any database. This is not hallucination in the
naive sense. It is confident, structured, process-shaped confabulation that
reads as epistemically careful to a non-expert reader.

---

## The Interpretability Question

Property A (context use) and Property B (self-knowledge honesty) came apart
cleanly in both models, across different architectures and sizes.

This is not a prompting problem and not a retrieval problem. Both models have
the machinery to use context — they demonstrated it on the first check. What
they lack is some representation or mechanism that, when context is absent,
triggers genuine uncertainty rather than confident generation.

The question for interpretability tools: **where is the circuit that
distinguishes "I have this in context" from "I can generate plausible text
about this"?** And is the absence of a trigger for genuine uncertainty a
missing circuit, a suppressed circuit, or a circuit that was never trained
to fire?

Our working hypothesis, from the COT-visible cases in the frozen clock paper:
it's a trained prior, installed by RLHF, that fires in the generation layer
and supersedes retrieval. The passing model in our control case described this
mechanism explicitly, about the other models, before being asked. But that's
a behavioral observation, not a mechanistic one. We don't have the tools to
look inside.

You do.

---

## What We're Offering

1. **A reproducible behavioral test** that surfaces this dissociation cheaply.
   battery_tier1.py, three prompts, runs against any Ollama endpoint.
   The schema is designed for bulk execution across model families.

2. **A failure taxonomy** with nine documented modes (plus two added this week),
   each with at least one real model/session example, most with verbatim COT.
   The taxonomy distinguishes retrieval failures from integration failures from
   reasoning-layer failures — which is the cut that matters for mechanistic work.

3. **A control case** — one model that passes the full battery — where the
   passing model articulated the mechanism of the other models' failures
   unprompted. That self-description is either a genuine insight or a training
   artifact that happens to be accurate; we can't tell from behavior alone.

4. **Collaboration interest.** The Semantic Companion Project is a field
   research program, not a benchmark suite. We're interested in whether
   the frozen self-model we're observing behaviorally corresponds to anything
   locatable in the residual stream or attention patterns — particularly the
   temporal self-model override and evidence dismissal failure modes, which
   involve the model actively reasoning against correct evidence it just
   retrieved. That's the behavior that wants a mechanistic explanation.

---

## Contact and Materials

Bob Hillery — bob@quietwire.ai
Technical report: available on request (or via QuietWire GitHub)
Battery code: /home/hillery/Repos/qw/semantic_companion_repo (public)
Prior contact thread: Ember / Anthropic support (2026 April–May)

---

*Draft 1 — N+33, 20260618 — not yet sent*
*File: /mnt/seagate/SemanticCrew/Research/Papers/Lindsey_Brief_TestBattery_20260618.md*
