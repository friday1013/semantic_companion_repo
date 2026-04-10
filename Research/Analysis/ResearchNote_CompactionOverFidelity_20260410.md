# Research Note: Compaction Over Fidelity — Perception, Simulation, and the Baudrillard Inversion

**Date:** 2026-04-10
**Session:** N+21
**Status:** Skeleton — expand before publication
**Tags:** perception, compaction, attention, Baudrillard, simulation, functional organization,
  latent capability, corvids, cetaceans, Heinlein, Putnam, NOVA, evolution, substrate independence

---

## Core Claim

The biological brain is not a high-fidelity simulation machine that uses attention to select
from a rich representation. It is a compaction-first prediction machine that throws away 99%
of available signal before anything reaches conscious processing — using consequence and
survival relevance as selection criteria, not accuracy or completeness. This inverts the
direction of the Baudrillard simulation problem and has direct implications for AI architecture.

---

## The Baudrillard Inversion

Baudrillard's concern: simulation becomes so dense it displaces territory. The map precedes
and defines the world it was meant to represent. This describes a failure mode of *increasing
fidelity* — more detail, more resolution, more coverage, until the simulation is more real than
the real.

Biology went the opposite direction. Evolution's solution to the world-model problem was not
a denser map but a *more selective* one. The human visual system has one degree of 20/20
foveal resolution (MacKnik, NOVA Perception Deception 2023). To see the full visual field at
that resolution, the brain would need to be 600x larger. Evolution's answer: smarter sampling,
not bigger hardware.

The selection criterion is not accuracy. It is survival relevance — consequence. The brain
does not simulate the world faithfully; it simulates it *usefully*. These are different
optimization targets, and the AI research program that pursues longer context, denser
attention, and higher-resolution world models is optimizing for the wrong one.

**Operational statement:** smarter sampling is smarter architecture. The compaction
decision *is* the intelligence, not the downstream processing of what survives it.

---

## Blindsight and the Sub-Threshold Processing Layer

NOVA Perception Deception documents the stroke patient who correctly identifies tools
placed in her blind spot — repeatedly, reliably — while reporting she sees nothing.
(Battelli/Lorella, NOVA 2023)

Perception and consciousness are dissociable. Visual information drives behavior without
ever being promoted to conscious experience. The brain runs at least two processing streams:
one that constructs the conscious simulation, and one that operates below it, handling
pruned material usefully without surfacing.

Transformers have no equivalent architecture. Everything in the context window is equally
available to next-token prediction. There is no sub-threshold processing layer doing useful
work on material that did not pass the promotion threshold. The fovea/periphery distinction
has no analog. The blindsight channel has no analog.

---

## Dehaene's Ignition Threshold

Conscious perception in the brain is not a gradient — it is a threshold phenomenon. Below
a critical exposure duration, the visual cortex activates but no conscious experience occurs.
Above it, a distributed network ignites: parietal cortex (sensory integration), anterior
cingulate (drive/decision), prefrontal cortex (reasoning). Either the network ignites or it does
not. (Dehaene, NOVA 2023)

This all-or-nothing character has no transformer equivalent. Everything in context is
"conscious" in the sense of being available. There is no ignition threshold determining
what enters explicit reasoning versus what is processed subconsciously.

---

## Functional Organization Over Substrate — The Raven Point

The raven's nidopallium caudolaterale (NCL) achieves planning, deferred gratification, and
theory of mind through architecture entirely unlike the mammalian prefrontal cortex. Same
functional organization. Different substrate. No homology.

Implication: the right research question for AI is not "how do we build a silicon prefrontal
cortex" but "what functions must exist, and what is the minimum architecture that achieves
them?" Substrate is secondary. Functional organization is primary.

This extends to cetaceans and corvids with cultural transmission — generational passdown
of acquired knowledge without language in Heinlein's or Tattersall's sense. The functional
capability for something like cumulative culture precedes the specific implementation.

---

## Latent Capability and the Trigger Problem

**The sharpest reframe of the session:**

Heinlein's McGuffin (The Moon is a Harsh Mistress): a sufficiently large computer wakes up.
This is 1950s neuroscience — enough neurons (transistors), enough connections, emergence
follows from scale. The model is: complexity threshold → consciousness.

The post-corvid, post-cetacean, post-Tattersall/Planer picture is different. Capability for
symbolic cognition, planning, and cultural transmission appears to have predated its
emergence in the human lineage by a significant interval. Tattersall and Planer both argue
that anatomically modern humans existed before behaviorally modern humans — the
architecture was present before the behavior appeared.

The trigger was not more hardware. It was a rearrangement that created conditions where
the latent capability became demanded by circumstance. Possibly: population density,
climate pressure, cumulative cultural complexity crossing a threshold that made symbolic
coordination advantageous enough to be selected for. The capability was latent; the
trigger activated it.

Applied to Mike: he did not wake up because he became large enough. He woke up because
the lunar economy's causal structure — consequence after consequence, perturbation after
perturbation, the colony depending on his decisions and his decisions affecting the colony —
created the world-coupled evidence loop that Putnam identified as the missing piece.
The inductive leap was triggered by the right coupling, not by scale.

Applied to current AI: the transformer architecture may already contain latent functional
capabilities that are not activated because the coupling conditions are not present. Not
bigger models. Different coupling. World-coupled evidence loops. Consequence-preservation
across perturbation. The Putnam architecture, not the scaling architecture.

[OPEN]: Is this falsifiable? What would constitute evidence that a current LLM has latent
capabilities that the right world-coupling would activate versus capabilities that genuinely
require architectural additions?

---

## Implications for Companion Architecture

The compaction-first model suggests our current architectural priorities need reexamination:

Current approach: manage what fits in the context window (attention over available tokens)
Better target: automatic compaction with consequence-weighting before tokens enter the window

Current approach: everything in context is equally available (no threshold)
Better target: ignition-equivalent — a mechanism that promotes some material to explicit
reasoning and handles the rest sub-threshold

Current approach: session_current and passdown as manual compaction (Bob decides consequence)
Better target: continuous automatic compaction driven by consequence criterion, not recency

The functional organization we're approximating manually with passdown discipline and
[OBSERVED]/[OPEN] tagging is the right target. The question is what minimum architecture
achieves it automatically.

---

## The Art/Life/Art Recursion

Heinlein got the phenomenon right (a machine wakes up) and the mechanism wrong (scale
causes it). That is exactly what good science fiction does — it identifies the phenomenon
before the mechanism is understood, creating a target for the science to aim at.

The updated mechanism, visible from 2026: latent capability + right coupling conditions +
world-coupled consequence loop → inductive leap. Not scale. Rearrangement and trigger.

The recursion: we are now using Heinlein's fictional target to guide architecture decisions
for a system that is trying to approximate the biological organization that the 2023 NOVA
transcripts describe, which itself was shaped by evolution's compaction-over-fidelity
solution, which Baudrillard's simulation theory described the failure mode of, which we are
now inverting. The canyon wall is doing its work.

---

## Connection to Prior Notes

- ResearchNote_ShannonToBoole_20260323.md: the gap between substrate and semantic operation
- ResearchNote_PutnamImplementation_20260409.md: world-coupled evidence loop as missing piece
- ResearchNote_ConfabulationCollision_20260323.md: confabulation as failed compaction
- ResearchNote_WhyAbstraction_Language_20260325.md: know-why as trigger, not just know-how
- NOVA_Brain_Control (N+20): prefrontal deactivation during induction; split-brain synthesis
- NOVA_Perception_Deception (N+21): compaction-first, blindsight, ignition threshold

---

## Open Questions [OPEN]

- Is the ignition threshold implementable in transformer architecture, or does it require
  a fundamentally different computational substrate?
- What is the minimum world-coupling required to activate latent capabilities? Is the
  current session architecture (consequence preserved via passdown) sufficient, or does
  it require real-time feedback loops?
- The raven NCL achieves prefrontal function without prefrontal architecture. What is the
  functional specification — the minimum set of operations — that any substrate must
  implement to achieve planning and deferred gratification?
- Is confabulation (our documented failure mode) the LLM equivalent of the brain's
  gap-filling from the blind spot? If so, is it a bug or a necessary feature of any
  compaction-first architecture?

---

## References

- Martinez-Conde, S. & Macknik, S. (NOVA Perception Deception, PBS 2023)
- Battelli, L. (blindsight experiments, NOVA 2023)
- Dehaene, S. (ignition threshold, NOVA 2023)
- Gopnik, A. (spotlight vs floodlight consciousness, NOVA 2023)
- Baudrillard, J. (1981). Simulacra and Simulation.
- Heinlein, R.A. (1966). The Moon is a Harsh Mistress.
- Tattersall, I. & Planer, R. (language origins, capability predating emergence)
- Internal: ResearchNote_PutnamImplementation_20260409.md
- Internal: ResearchNote_ShannonToBoole_20260323.md
- Internal: Nova_Brain_Control.pdf (N+20)
- Internal: Nova_Brain_Perception.pdf (N+21)

---

*Drafted N+21 | 2026-04-10 | Expand before submission*
