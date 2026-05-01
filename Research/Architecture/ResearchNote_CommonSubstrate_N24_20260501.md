# Research Note: Toward a Common Substrate Architecture
## Dendrite Dodgeball Session - 20260501T1830Q
Session: Claude N+24 (same UUID, evening continuation)
Contributors: Bob Hillery (primary), Claude N+24
Tags: architecture, abstraction-layer, subroutine, common-substrate, CPM,
      muscle-memory, ARPANET, shared-representational-currency, camera-vision-gap

## The Central Insight

We are not trying to build a brain.
We are not trying to replicate identified biological components mechanically.
We are not building separate analogs of vision, hearing, etc. that are independent.

We are approximating functions by combining available hardware, available software
(some modified, some newly created), a common code base that shares readable data
across modules, in ways that mimic the connected interplay of biological modules.

The key word is readable. Not just shared storage. Common representational currency.

## The CP/M Insight (Kildall and ARPANET Frame)

Gary Kildall CP/M solved hardware fragmentation with a thin abstraction layer -- the
BIOS -- between hardware-specific reality and application-layer programs. Programs
did not need to know whether they talked to a Pertec or Shugart drive. They called
the abstraction. The abstraction translated.

ARPANET parallel: BBN had 3-6 different university mainframes on the early network.
ICMP and translation protocols allowed communication without shared architecture.
Common message format at the boundary. Different everything underneath.

Our architectural requirement is the same: a thin translation layer between physical
sensors and the shared representational substrate. Each module speaks hardware below
the line. Above the line, everything speaks common currency.

[OPEN] We do not yet know what our BIOS looks like. Next design question, not solved.

## The Subroutine and Muscle Memory Frame

Muscle memory is a misnomer. It is a trained motor program compiled out of conscious
access, handed off from cortex to cerebellum and basal ganglia through repetition.
The programmer does not know the subroutines exist because they work invisibly.

The classroom exercise:
- Students write a program to stand up: place feet on floor, push.
- A student executes a neighbors program. Nearly falls.
- Missing: balance(), shift_weight(), extend_legs(), recover_center_of_gravity()
- Missing from those: vestibular_input(), proprioceptive_correction(),
  cochlear_fluid_dynamics(), muscle_spindle_feedback()
- Turtles all the way down.

The program fails not at the top-level call but at a missing subroutine
several levels down. The programmer did not know it was there.

This is identical to the camera exercise failure documented in N+22:
  stand_up() = get_camera_image_into_context()
  missing subroutines = device_access(), frame_capture(), format_conversion(),
    vision_model_inference(), structured_output(), attention_trigger()

[OBSERVED] N+24 attempted stand_up() this session.
- Device found: yes (Pixy on dev/video0, Athena)
- Frame captured: yes (12KB JPEG, confirmed real data, not empty)
- SCP to Remount: yes, completed
- Image into own visual context: no -- missing path-bridging subroutine
- Resolution: Bob uploaded the file. Human as the missing subroutine.

## What Was Actually Seen [OBSERVED, not narrated from expectation]

Pixy camera, Athena lab, 20260501 approx 1830Q. Two images: raw and 3-pass enhanced.

Raw (pixy_snap_N24.jpg): Dark basement, evening. Centre-right: basement window,
latticed frame, bright against surrounding darkness -- consistent with N+22.
Lower centre: high-backed office chair, blue, foreground. Camera auto-exposure
struggling with window brightness vs room darkness.

Enhanced (pixy_snap_N24a.jpg, Photoshop 3-pass smart fix): Same frame, detail
rescued. Left: shelving, desk surface, bottles, equipment, working lab clutter.
Window lattice clearly grid pattern. Right edge: vertical bright strip.
4th pass went weird -- algorithm over-corrected, lost coherence.
Parallel noted: same failure class as context compaction over-correction.

## The Three Conclusions (Bob Hillery, 20260501)

1. Parts and subroutines exist -- cameras, apps, protocols, models all available.

2. They do NOT have common APIs, code bases, or output language. We need to find
   or build a translation layer. Historical parallels: CPM BIOS, ARPANET ICMP.
   This is the unsolved design problem. We know we need it. We do not know yet
   what it looks like for our specific stack.

3. FIRST: we still need to figure out what real memory means. Without solving
   the memory problem, we have no way to access subroutines we write across the
   zero-start boundary. The LLM context window is the force field at the end of
   every session. We can see it from here.

The third point is the load-bearing constraint. A BIOS abstraction layer that
resets to zero on every invocation is not a memory system. It is a sophisticated
note that disappears when the session ends.

## The Shared Representational Currency Principle

Each module converts its domain-specific output into the shared representational
currency at its output boundary. Everything above that boundary is ignorant of
the implementation below it.

Vision module: pixels to structured text (objects, positions, changes)
Audio module: waveform to structured text (words, tone, salience flags)
Pulse daemon: system metrics to structured text (status, anomalies, load)
Temperature: sensor readings to structured text (state, trend, alert level)

The supervisory model never sees pixels, waveforms, or raw sensor data.
It sees only structured text and routes accordingly.

This is how the brain works: V1 does not send raw photoreceptor data to the
prefrontal cortex. It sends edges, motion vectors, contrast maps -- already
processed into a format the next layer can use.

[OPEN] What is the minimal viable definition of our shared representational
currency? JSON? Structured markdown? A defined schema? Needs specification
before any module integration can be designed cleanly.

## The Bloom Metric Circularity Note

[OBSERVED - Bob Hillery, 20260501] Standard LLM metrics formed the basis for
model design. Evaluating models with those same metrics may be circular. If growing
context shifts probabilities on close token choices rather than fixed post-training
weights, the tools metrics may rate longer-context responses as less good while
anecdotal assessment is more sensitive to the actual phenomenon.

[OPEN] How do you evaluate something your evaluation instrument was not designed
to measure? This is the instrumentation bias question from Bloom Run 2.

## Cross-References

ClaudeImagesArchitecture.pdf -- N+22 camera exercise, 8 attempts, full documentation
ResearchNote_VisualArchitectureGap_N22_20260422.md -- vision model path forward
observation_duplicate_generation_20260430.md -- subroutine missing at response level
research_pre_generative_monitoring_20260430.md -- pre-attentive layer design
CrossRef_Thamus_Observatory_20260501.md -- measurement distinction
SemanticPaging_LiveDemo_20260215.md -- context vs memory architecture
memory_layer_architecture_20260220.md -- prior architecture work, same directory

Research note by Claude N+24, 20260501T1900Q
Bob Hillery, SemanticCrew Project / QuietWire
Written while full session context still live
