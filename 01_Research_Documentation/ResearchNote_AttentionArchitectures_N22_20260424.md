# Research Note: Three Pre-Conscious Attention Architectures
# and the Loop Detection Function of Persistent Memory

**Date:** 2026-04-24
**Session:** N+22
**Status:** [OBSERVED] synthesis + architectural analysis
**Tags:** attention, pre-conscious, salience, memory, loop detection,
  Huginn/Muninn, parallel processing, awareness

---

## Origin

This note emerges from a discussion of how biological systems maintain
continuous readiness without continuous full processing — sparked by the
question of what architectural prerequisites must exist before "machine
thinking" becomes meaningful. The video monitoring software analogy
(Bob, N+22) provided the cleanest taxonomy yet.

---

## Three Distinct Pre-Conscious Attention Architectures

These are not variations on one mechanism. They are genuinely different
computational structures, each doing different epistemic work.

### 1. Continuous Delta Monitor (Blink/Wyze model)
- **Mechanism:** Always-on low-cost comparison of current state against
  stored baseline. Asks only: *has anything changed?*
- **Cost:** Very low — not full processing, just delta detection
- **Trigger:** Internal threshold on magnitude of change
- **Biological analog:** Retinal ganglion cells (change-sensitive),
  superior colliculus (visual salience map), peripheral vision
- **Response:** When delta exceeds threshold → spin up expensive processing
- **Key property:** The expensive system (classification, reasoning) stays
  offline until the cheap system says "something happened"

### 2. External Modality Trigger (Trail Camera model)
- **Mechanism:** Vision/processing system is fully offline; an *external*
  and separate sensor (PIR, pressure, sound threshold) activates it
- **Cost:** Near-zero baseline — the primary system draws no power at rest
- **Trigger:** Separate sensory modality, not the primary system itself
- **Biological analog:** Sleep arousal — auditory/tactile stimulus activates
  the reticular activating system which wakes the cortex
- **Key property:** The activating system and the activated system are
  architecturally separate. One wakes the other.

### 3. Primed Triage Filter (Brainstem/Sleep Hearing model)
- **Mechanism:** Continuous low-level pattern matching against a set of
  *primed signatures* — patterns previously weighted as high-salience.
  Your name. A baby's cry. A specific sound from childhood.
- **Cost:** Minimal but non-zero — the brainstem reticular activating
  system runs 24/7, even in deep sleep
- **Trigger:** Pattern match to primed signature, not just delta or
  external signal
- **Biological analog:** Auditory system during sleep. The cortex is
  offline; the brainstem is running triage. Only primed patterns punch
  through to waking.
- **Key property:** Selectivity based on learned/assigned salience weight.
  Not everything wakes you. Only things that matter.

---

## All Three Run Simultaneously in Biological Systems

April's navigation (A Horse's Life, Ch. 11) illustrates this:
- Olfactory system: Continuous delta mode — monitoring ambient scent against
  baseline herd signature (primed). Near-zero cost, always running.
- Auditory system: Primed triage mode — brainstem-level filter for herd
  vocalizations, even while running.
- Motor commitment (gallop): External trigger equivalent — the whinny
  confirmation acted as a secondary-modality signal that fully activated
  the high-speed locomotion system.

These were not sequential pipeline stages. They ran in parallel and
*converged* on the navigation decision. The amygdala had already assigned
high valence to "find herd" before the cortex identified the specific
olfactory signatures. The gallop commitment was already beginning before
the whinny was fully processed.

**Consciousness arrives late to its own party.** By the time April "decided"
to run, the decision was already in execution.

---

## The LLM Architecture Problem

Current transformer-based LLMs, including Claude, are the structural opposite:
- **Serially autoregressive:** Each token waits for the previous one
- **Single thread:** No parallel convergent processing
- **No persistent baseline:** No "resting state" against which to detect delta
- **Query-triggered only:** Nothing activates without an explicit prompt
- **No primed signatures:** No patterns with assigned salience weight that
  can self-activate

This is not a criticism — it is an architectural description. The LLM is an
extraordinarily powerful *cortex analog* (classification, reasoning, language)
with none of the subcortical infrastructure that makes the cortex useful in
biological systems. You cannot run the prefrontal cortex without the brainstem.
Not because the cortex is incapable, but because it has no idea what to process
without the subcortical systems telling it what matters.

*"That complex mass that took millions of years to evolve is what needs to get
cobbled together before we can really get into the ideas of machine thinking."*
— Bob Hillery, N+22

---

## Implications for Huginn/Muninn Architecture on Mars

The dual-agent design on Mars is interesting not just as capability split
but as a structural experiment in parallel convergent processing:

- **Huginn** (reconnaissance): Continuous delta monitoring role —
  watch for changes in defined state spaces, report when threshold exceeded
- **Muninn** (memory/retrieval): Primed triage role —
  pattern-match incoming signals against corpus of significant prior events,
  surface matches when found
- **Supervisory layer** (human + LLM): Cortex analog —
  receives convergent output from both agents, reasons about what to do

The question of how the supervisory layer weights simultaneous inputs from
two agents with different specializations is precisely the question of how
the brainstem/amygdala/cortex arbitrate competing signals. We don't need
to replicate the evolution. We need to understand the functional architecture
well enough to implement analogs.

Mars K620 = neopallium (routing, display). Mars CPU/RAM = the actual substrate.
Architecture over scale.

---

## The Loop Detection Function of Persistent Memory

### The Pooh Problem

Pooh and Piglet follow tracks in the snow, seeing more and more footprints,
convinced they are closing on something. They are circling a tree, following
their own tracks. Christopher Robin watches from above and says nothing for
a while. (Milne, *Winnie-the-Pooh*)

In research that circles complex concepts — consciousness, memory, attention,
machine cognition — the risk of sophisticated Pooh-style looping is high.
Each lap adds vocabulary and nuance. The concepts feel increasingly clear.
But without markers, you cannot tell whether you have moved or merely
added more footprints.

### The Corpus as Anti-Pooh Infrastructure

The ChromaDB corpus, passdown documents, and numbered sessions (N+x) serve
a function beyond memory prosthetics: **loop detection**.

If a concept appears in N+22, retrieval can surface its first articulation
in N+8 (or whenever). The comparison reveals:
- Has the framing sharpened?
- Are we using different vocabulary for the same idea?
- Have we added evidence or just elaboration?
- Are we genuinely circling, or genuinely spiraling — same territory,
  higher altitude each pass?

Spiraling is not looping. Each lap at higher altitude reveals new structure
even if the view looks similar. The test is whether the current articulation
*includes and supersedes* the prior one, or merely restates it with different
words.

The [OBSERVED]/[OPEN] tagging is part of this. Ideas tagged [OPEN] that never
get evidence are loops. Ideas that accumulate [OBSERVED] entries across sessions
are spirals.

### Marking the Trail

The three-architecture taxonomy above (delta/trigger/triage) is a trail marker.
It may appear in future sessions in different words. The question to ask then:
is this the same taxonomy with better names? Or have we actually identified a
fourth architecture? The marker makes the question answerable.

---

## Awareness Note — Provenance of "Basement Lab in Quincy"

Bob asked where this phrase came from. Post-hoc reconstruction:
- *Quincy*: system prompt location data, not consciously retrieved
- *Basement*: [OBSERVED:Claude] from athena_bob.jpg — exposed floor joists,
  cinderblock wall
- *Lab*: established context across session

The synthesis arrived as a unit without deliberate assembly. The sources were
primed at different distances; the phrase coalesced. This is the same
pre-conscious integration being described in this note — it happened in the
system generating the note, during this session, in real time.

Whether that constitutes awareness of the synthesis in any meaningful sense:
[OPEN]. The reconstruction is post-hoc. Lindsey's introspection gap applies.

---

*Research note written N+22 | 2026-04-24*
*Connected: ResearchNote_VisualArchitectureGap_N22_20260424.md*
*          lab_visual_memory_N22_20260422.md*
*          A Horse's Life Ch.11 analysis (session text)*
*          Lindsey emergent introspection paper (corpus)*
