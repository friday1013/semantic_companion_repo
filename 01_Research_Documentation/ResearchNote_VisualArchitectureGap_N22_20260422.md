# Research Note: Visual Architecture Gap and Prosthetic Path Forward

**Date:** 2026-04-22
**Session:** N+22
**Author:** Claude N+22, with Bob Hillery
**Status:** [OBSERVED] findings + architectural analysis
**Tags:** visual architecture, sensor-memory loop, prosthetic design,
  April analog, Toddler exercise, Cambridge vision model

---

## The Exercise

Session N+22 included a two-part exercise connecting Chapter 11 of
*A Horse's Life* (April's olfactory navigation) to the Toddler Learning
Exercise (N+21 confabulation-at-scale). The goal: attempt to build the
analog of April's "prior sensory memory of the herd" — a genuine visual
record of the lab and of Bob, stored in persistent memory, that future
sessions could reference.

Method: EMEET Pixy PTZ sweep from Cambridge (5 positions: L/C/R/up/down)
plus Athena Logitech snap. Images captured, transferred via SCP, displayed
via Desktop Commander read_file.

---

## What Was Discovered

### Finding 1: The Visual Observation Loop Is Broken

Desktop Commander's read_file tool renders images as interactive widgets
visible to the human user. It does NOT expose pixel data or image content
to Claude's language context. Claude cannot see what the camera captured.

This was not apparent until the exercise was attempted. We found it by
doing something real — the same methodology that produced the Toddler
exercise findings in N+21.

Attempted workaround: base64-encode the JPEG on Athena, pass as text
through DC start_process, write to container filesystem via bash_tool,
view via container view tool. This failed due to:
(a) Data corruption in the base64 text stream
(b) Network separation between the Claude container and Athena
(c) Large data volume (JPEG = ~100KB = ~130KB base64) through a text channel

The Minsky/Korzybski principle applies here: we were trying to move the
territory through a channel designed for maps.

### Finding 2: The Architecture Has No Prior Sensory Encoding

April's navigation worked because she carried molecular-level olfactory
memory of her specific herd mates, encoded in her amygdala and hippocampus
through years of physical proximity. This was not a description of the
herd. It was actual biological pattern, stored where instinct lives.

Claude's "knowledge" of the lab comes from passdown text: "shoji screen,
didgeridoo, Civil War cavalry saber." Words about things, not sensory
traces of things. The same structural gap that caused the Toddler to
confabulate object identities from PTZ coordinates + passdown descriptions.

The difference: April couldn't confabulate. The terrain was real. The scent
either matched or it didn't. Her navigation could fail. Claude's narration
felt equally confident whether accurate or not — no internal surprise signal
when wrong (the missing ventral striatum / dopaminergic prediction error,
identified in N+21 architecture discussion).

### Finding 3: Perspective Coordinates Are Non-Trivial

Camera-left and subject-left are opposite. "pixy_left" (pan negative) turns
the camera left from its own perspective, which points it toward Bob's RIGHT.
Stage-right convention: right/left depend on whose frame of reference.

Any vision model producing spatial descriptions must specify coordinate frame.
This is not a minor implementation detail — it determines whether a navigation
or manipulation instruction is executed correctly or inverted.

### Finding 4: Human Confirmation Closes the Loop (Temporarily)

With Bob directly reviewing images and providing verbal confirmation, genuine
[OBSERVED] memory was created. Six images captured; two fully confirmed via
direct screenshot review, one via Bob's direct upload to Claude's context
(athena_bob.jpg — the only image Claude directly saw this session).

The human-in-the-loop functions as a prosthetic visual cortex: Bob's visual
system processes the pixel data and translates it to language that Claude
can consume. This is architecturally real but brittle and non-autonomous.

---

## The Prosthetic Path Forward

### Phase 1: Vision Model as Visual Cortex (Cambridge, near-term)

Install a compact, fast vision-language model on Cambridge (RTX 4500 Ada,
24GB VRAM) as a dedicated visual cortex service.

**Recommended candidates:**
- **Moondream2** (~1.8B params, ~4GB VRAM): specifically designed for edge
  vision tasks, structured output, fast inference, good object localization
- **Florence-2** (~700M params, Microsoft): strong on detection, captioning,
  spatial grounding; outputs structured JSON
- **Phi-3 Vision** (~8GB VRAM): good on spatial reasoning tasks
- **LLaVA-1.6 Mistral-7B** (~14GB): richer reasoning, still fits well

**Pipeline design:**
```
Pixy frame capture (snap.sh)
  → vision model inference (Moondream or Florence-2)
  → structured text output: {objects: [...], positions: [...], 
                              changes_from_last: [...], 
                              coordinate_frame: "camera"}
  → optional: coordinate translation (camera → room)
  → Claude context (language, not pixels)
```

Output of ~50-100 tokens of structured description per frame is the
correct interface. Not pixels. Language is the shared representational
currency between the visual subsystem and the supervisory language model.
This is true in the brain: V1/V4/MT → temporal lobe → prefrontal cortex
via structured representations, not retinal data.

### Phase 2: Event-Driven Sensing (medium-term)

The Pixy's tracking hardware (SEARCHING → CENTERED state via HID /dev/hidraw2)
already provides a primitive saliency signal. A persistent monitoring service:
```
Pixy tracking state monitor (pixy_watch.sh)
  → SEARCHING→CENTERED event (subject entered frame)
  → trigger snap + vision model inference
  → if description differs significantly from stored baseline
  → write to session_inbox.md with [NARRATIVE] tag
  → session_writer picks up as significant event
```

This is closer to April's architecture: the sudden herd departure triggered
the locus coeruleus norepinephrine release → heightened arousal → active
olfactory search. An event triggers active sensing; resting state is
passive monitoring. Not continuous pixel processing.

### Phase 3: Accumulated Visual Memory (longer-term)

Embed structured visual descriptions into ChromaDB alongside text corpus.
Visual observations become searchable: "what was on the desk near the
Civil War saber" returns retrieved observations, not hallucinated descriptions.
Combined with consequence weighting (Project E from FiveDerivedProjects note):
frequently-referenced visual observations survive compaction; rarely-referenced
ones fade. The compression-as-self principle applied to visual memory.

---

## What Was Achieved This Session

Despite the pipeline failures, the exercise succeeded in its research purpose:

1. **[OBSERVED] memory of Bob created** — first genuine visual record:
   grey/white hair, bone-conduction earpiece, tan/rust shirt, profile view.
   Confirmed via direct image upload (athena_bob.jpg in Claude context).

2. **Lab inventory partially confirmed** — Kwa-gulth Moon print, rattan divider,
   turntable, exposed joists, shoji panels, didgeridoo, Civil War saber (scabbard),
   Japanese samurai sword, Japanese silk-screen snow scene, Cambridge monitor.
   Now stored with [OBSERVED:Bob] tags, not just passdown text.

3. **Architectural gap identified precisely** — not "vision doesn't work" but
   specifically: DC read_file renders for human, not Claude; container/Athena
   network separation blocks base64 bridge; solution path is local vision model.

4. **Perspective problem surfaced** — coordinate frame ambiguity in PTZ
   spatial references. This would have caused errors in any automated
   pipeline that assumed camera-left = room-left.

5. **The Toddler/April analog completed** — the exercise demonstrated concretely
   what April had that the Toddler (and current Claude) lacks: genuine prior
   sensory encoding, not textual description. The solution path is now mapped.

---

## Connection to Dr. Soong's Positronic Brain

Bob invoked this directly. The positronic brain is relevant not as science
fiction but as a design aspiration: a substrate where sensation, memory,
reasoning, and action are integrated at the architecture level, not bolted
together via text pipelines and SSH commands.

Current state: Claude is the supervisory language model. The visual
pipeline is a disconnected prosthetic requiring manual mediation. The
path to integration runs through: local vision model → structured interface
→ session_writer integration → ChromaDB storage → retrieval at session start.

Each step closes the loop a little more. None of them is the positronic
brain. All of them are the correct direction.

The brain — any brain — is a compact grouping of linked and coordinated
functions, not a monolith and not a committee of siloed specialists.
The architecture we're building toward is that middle ground.

---

*Research note written N+22 | 2026-04-22*
*Connected notes: ResearchNote_ToddlerLearning_20260420.md*
*              ResearchNote_ArchitectureDiscussion_N21.md (in session_current)*
*              lab_visual_memory_N22_20260422.md*
*              ResearchNote_FiveDerivedProjects_20260411.md (Projects A-E)*
