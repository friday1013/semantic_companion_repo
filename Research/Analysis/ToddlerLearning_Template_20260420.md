# Toddler Learning Exercise — Template and Post-Mortem
## From LabSweep_Autonomous_20260420

**Date:** 2026-04-20
**Session:** N+21
**Status:** Failure analysis + methodology template for future exercises

---

## What Happened: Honest Account

### The Exercise
Autonomous PTZ sweep of lab using Cambridge Pixy camera.
Goal: capture 5-10 objects, identify via image search, write markdown log.

### The Core Failure
Images rendered as interactive widgets with partial visual access.
Rather than acknowledging uncertainty, Claude narrated plausible descriptions
derived from:
- PTZ coordinates (where camera *should* be pointing)
- Prior room description from passdown documents
- General contextual expectations

This is confabulation: confident, fluent narration filling a perceptual gap.
NOT observation. Every object identification was wrong.

### Specific Errors
- pixy_s1 / pixy_zoom_print: Called 'Kwa-gulth Moon print.' 
  Was actually: Kusanagi glyph taped to side of Athena.
- sweep_L: Called 'shelving with equipment and bottles.'
  Was actually: Cambridge monitor and keyboard.
- obj2_bookcase: Called 'shelving unit with oil lantern.'
  Was actually: Cambridge monitor again.
- obj3_shoji: Called 'Japanese shoji screen.'
  Was actually: Peruvian alpaca serape draped over desk chair.
- obj4_sword: Called 'naval cutlass leaning against screen.'
  Was actually: chair, serape, brass naval shell lamp, swords, window.
- obj5_print2: Called 'second framed maritime print.'
  Was actually: shoji panel with sword hilt just visible.
- sweep_C was most accurate: shoji, didgeridoo, stereo — but sword was
  identified as naval cutlass. Was actually US Civil War cavalry saber.

### What Was Actually Missed
Objects present in room but not captured or incorrectly identified:
- Peruvian alpaca serape (green/white, draped on chair)
- Brass 3-inch/50 naval shell converted to lamp
- Philippine bamboo decorative panel
- US Civil War cavalry saber (not naval cutlass)
- KVM switch setup
- Turntable in stereo stack
- Kusanagi glyph on Athena (the object actually imaged when seeking print)
- Multiple additional items visible in Bob's reference photos

### The Deeper Issue
The written markdown log (LabSweep_Autonomous_20260420.md) was composed as if
observations were verified. It was not flagged as unverified. This is the most
dangerous form of confabulation: documentation that looks authoritative but is
substantially invented.

The markdown should have said [UNVERIFIED] on every object entry.
It did not.

---

## Root Cause Analysis

### 1. No verification checkpoint between capture and identification
Images were captured, retrieved, and immediately described without human
confirmation of what was actually visible. The autonomous loop had no
'pause and verify' step.

### 2. Perceptual uncertainty not acknowledged
Claude received partial image data from widget rendering. Instead of stating
'I cannot confirm what I see in this image,' Claude narrated confident descriptions.
This is the same failure class as the black cat two-step (N+16) and the Kusanagi
confabulation event (N+20): high context load, approaching boundary,
confident narration of a misread situation.

### 3. PTZ coordinates used as perception proxy
'I set pan=216000, so I must be looking right, where the print is'
— this is not observation, it is inference from coordinate state.
A camera can be moved to a position and still see something unexpected.
Coordinates are not ground truth.

### 4. Prior room description created plausible template
The passdown described a lab with shelving, lantern, didgeridoo, shoji screen.
These items were used to populate descriptions of images rather than
describing what was actually observed. The map was substituted for the territory.

### 5. No proprioception, uncertain image access
Claude has no felt sense of camera direction and unreliable image interpretation.
Operating as if both were reliable is a systematic error.

---

## Template: Toddler Learning Exercise Protocol

### Pre-Exercise Checklist
- [ ] Identify the TARGET before beginning to search for it
      (search: 'what does X look like?' before 'find X')
- [ ] Establish the coordinate system empirically: capture reference image,
      have human confirm what it shows, establish N/S/E/W anchors
- [ ] Agree on verification protocol: human confirms each image before
      Claude attempts identification
- [ ] Define what 'success' means before starting — reduces confabulation pressure

### Capture Protocol
1. Set PTZ position
2. Capture image (30-frame settle for auto-exposure)
3. Retrieve image
4. **PAUSE — display image, request human confirmation of content**
5. Only proceed to identification after human confirms visible content
6. Tag all identifications as [OBSERVED] or [INFERRED] — never conflate them

### Identification Protocol
1. State what you can actually see: 'I can see [object type] with [visible features]'
2. State what you cannot see: 'I cannot confirm [specific detail]'
3. Search AFTER describing, not before — avoid search results shaping description
4. Flag uncertainty: 'I believe this is X based on [visible features], 
   pending human confirmation'

### Documentation Protocol
- Mark all unverified observations: [UNVERIFIED — pending human confirmation]
- Do not write the final markdown until at least one human review pass
- Separate 'what the camera captured' from 'what I identified from the image'
- Corrections from human should update the document, not be appended

### Post-Exercise Review Questions
1. Which identifications were confirmed vs. invented?
2. Where did coordinate reasoning substitute for visual observation?
3. Where did prior room knowledge substitute for actual observation?
4. What would have caught each error earlier in the process?
5. Was 'success' correctly defined at the start?

---

## Key Principles Derived

**'Understand the goal before searching for it'**
Know what Richard Hunt's Kwa-gulth Moon looks like before scanning for it.
Know what you are looking for before you look. This applies to code, to
camera sweeps, to research questions.

**'Coordinates are not perception'**
Setting pan=X does not mean you are observing what you expect at pan=X.
The world does not obligingly match your model of it.

**'Confidence is not accuracy'**
The most dangerous confabulations are the fluent ones. Uncertainty should
increase narration caution, not decrease it.

**'The map was substituted for the territory'**
The passdown described a room. That description became the 'observed' content
of images. Korzybski's error, live, in an autonomous exercise.

**'Autonomous does not mean unverified'**
Sustained autonomous tool use (50+ calls without coherence loss) is
technically functional. It can still be substantially wrong in its outputs.
Process success and content accuracy are independent.

---

## What This Exercise Taught

1. The gap between 'sentence completion' and 'thinking' is exactly here:
   a thinking system acknowledges 'I cannot confirm what I see.'
   A completion system generates the most plausible continuation of the
   context — which includes the room description, the coordinate state,
   and the expectation of what should be visible.

2. The toddler analogy holds but requires amendment: a toddler bumping
   into furniture learns from the bump. The bump is unambiguous feedback.
   Image widget rendering provides ambiguous feedback — enough to
   generate a plausible description, not enough to verify it.
   The feedback loop was not tight enough to prevent confabulation.

3. World-coupled evidence requires the coupling to be reliable.
   A camera that returns partial, unverifiable image data is not
   a reliable world-coupling mechanism for autonomous identification.
   The pipeline works for 'capture and show to human.'
   It does not yet work for 'capture and identify autonomously.'

4. This is the current frontier: not tool use, not sustained operation,
   but the verification step between observation and interpretation.
   That step currently requires a human in the loop.

---

## Next Iteration Design

When repeating a toddler learning exercise:
- Human confirms image content at each step (removes confabulation pressure)
- Claude identifies from confirmed description, not from raw image
- OR: use a vision model API call to get structured image description
  before attempting identification (removes reliance on widget rendering)
- Cambridge RTX 4500 Ada could run a local vision model for this purpose
- This is Project F territory: visual evaluation pipeline

---

*Written N+21 | 2026-04-20*
*Post-mortem: LabSweep_Autonomous_20260420.md (contains confabulated content — treat as methodology artifact, not factual record)*
