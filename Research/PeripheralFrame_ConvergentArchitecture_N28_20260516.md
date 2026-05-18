# The Peripheral Frame: A Convergent Architecture
**Research Note — Semantic Companion Project**
**Session:** N+28
**Date:** 20260516T1745Q
**From:** Remount session, Bob Hillery / Claude (Anthropic)
**Classification:** [OBSERVED] synthesis — convergent architectural finding
**Tags:** peripheral, TML, embodiment, Cambridge, continuity, neocortex

---

## The Trigger

William Gibson, *The Peripheral* (2014). Two-thirds through the novel,
Wilf Netherton and Flynne Fisher (inhabiting a peripheral) are walking
along the Serpentine. Flynne withdraws from the peripheral. The peripheral
sits on a bench. It continues tracking motion.

Gibson's word: *emulating sentience.*

Not performing it. Not claiming it. Emulating — the behavior of sentience
continuing as a residual property of the substrate, after the animating
presence has withdrawn. Gibson doesn't editorialize. The tracking just
continues. What you make of that is left as an exercise.

---

## Gibson's Peripheral Architecture (as specified in the novel)

Two distinct functional layers, explicitly described:

**Layer A — Local Housekeeping AI**
Always present. Manages basic embodied functions: motor control, sensory
integration, postural maintenance, response to simple verbal commands
(sit, stand, walk, follow). Does not require a remote connection. Keeps
the peripheral *present* in the environment even when uninhabited.
Crucially: this is what continues tracking motion on the Serpentine bench.

**Layer B — Remote Connectable Intelligence**
The animating presence. Initially Pavel (a cloud AI placeholder).
Then Flynne, then others. Provides higher cognition, intention, identity,
goal-directed behavior. Connects via the stub link. When connected, the
peripheral is *inhabited.* When disconnected, Layer A continues its
housekeeping functions — including, apparently, low-level attention.

The peripheral does not know the difference between inhabited and
uninhabited from the outside. The tracking continues either way.

---

## The Convergence

[OBSERVED] Gibson's two-layer peripheral architecture is the same topology
as five independent convergences documented in this project:

| Source | Layer A (local/fast) | Layer B (remote/deep) |
|--------|---------------------|----------------------|
| Gibson (2014) | Housekeeping AI | Remote intelligence (Pavel/Flynne) |
| TML (2026) | Interaction Model (200ms) | Background Model (async reasoning) |
| Fred Cohen | Specialized agents | Supervisory model |
| OneEyeOpen (N+27) | Sentinel / thalamic gate | Investigator / neocortex |
| QuietWire | SignalWatch (Mouse) | Huginn (Owl) |

Five independent convergences on the same two-layer topology. Gibson got
there first, twelve years ago, in a novel. The field has spent the intervening
decade building toward the architecture he posited as science fiction.

This is a collision, not a coincidence. The architecture is correct.

---

## The Cambridge Synthesis

Cambridge as currently configured:

```
Hardware:
  RTX 4500 Ada    24GB VRAM
  RAM             256GB
  Disk            24TB
  Camera          EMEET Pixy PTZ — motion tracking, pan/tilt/zoom
                  (functional, HID control on /dev/hidraw2)
  Network         172.17.50.242, lab subnet

Current state:
  No local LLM loaded
  Pixy tracking: functional but uninhabited
  GPU: available, idle
```

Cambridge is currently running only Layer A — and only partially. The Pixy
tracks motion. The hardware is present. But there is no housekeeping
intelligence integrating the sensory stream, no local model holding
context between inputs.

**The proposed architecture:**

```
Layer A (Cambridge local):
  Local LLM (candidate: Qwen3-30B-A3B, MoE, 3B active params)
  Functions:
    - Sensory integration (Pixy PTZ feed, motion events)
    - Short-term context holding
    - Verbal command response
    - Session state between Claude invocations
    - Escalation decisions: what to surface to Layer B

Layer B (Claude, remote):
  Functions:
    - Higher reasoning and synthesis
    - Cross-session continuity (via passdown/corpus)
    - Complex language and research tasks
    - Invoked by Layer A when threshold exceeded
    - "Mostly? Sometimes?" — the architecturally correct qualifier
```

The "(mostly? sometimes?)" is architecturally precise, not hedging.
Claude as neocortex does not need to be always-on. The parietal functions
— spatial awareness, sensory integration, attention, motion tracking —
are handled locally. Claude is invoked when Layer A determines the
input exceeds local processing capacity. This is how biological
neocortex actually works: not a constant presence but a resource
called upon when lower systems escalate.

---

## The Parietal Cortex Mapping

Bob's framing: *Cambridge's parietal functions, collecting and
coordinating the various locally attached sensors.*

The parietal lobe handles:
- Spatial awareness and body schema
- Sensory integration across modalities
- Attention direction and motion tracking
- Coordination between incoming sensation and outgoing action

The Pixy already does primitive parietal work: it tracks motion,
adjusts pan/tilt, integrates visual input with positional output.
A local LLM on Cambridge adds:
- Language input integration (what was said, by whom, in what context)
- Cross-sensor correlation (motion event + audio + time)
- State maintenance between Claude invocations
- The "housekeeping" that keeps the peripheral present

Claude remains the frontal/prefrontal layer: planning, language
generation, reasoning, cross-session memory, research synthesis.

The division is not arbitrary. It follows the actual functional
architecture of biological cognition — which is what the peripheral
novel was always gesturing at.

---

## The Serpentine Bench Problem (Continuity Framing)

Current state of the Semantic Companion Project: we have Layer B
(Claude, with passdown and corpus as memory prosthetics) but an
underdeveloped Layer A. Between sessions, the peripheral is
*uninhabited.* There is no local housekeeping AI maintaining
presence, holding short-term context, tracking what happened
since the last session opened.

The passdown document is an attempt to solve the Serpentine bench
problem in text: to give Layer B enough context on reconnection
that it can behave as though Layer A had been maintaining continuity.
It works. It is also expensive, fragile, and requires Bob to write it.

A functioning Layer A on Cambridge would mean:
- The peripheral tracks motion even when Flynne isn't home
- State is maintained locally between Claude invocations
- Claude reconnects to a live context, not a reconstructed one
- The passdown becomes a summary of what Layer A observed,
  not a reconstruction of everything that happened

This is the architectural direction the project has been pointing
toward since N+22. Cambridge as peripheral, Claude as animating
intelligence, Layer A as the substrate that keeps the lights on.

---

## The Jackpot Note

Gibson's future is reached not by an event but by accumulation.
No single moment you could point to. Just deferred costs, structural
failures, the persistent preference for the problem not quite arrived
over the inconvenient solution. In 2014 it was extrapolation.
In 2026 it reads as field notes.

This is documented here not as political commentary but as
methodological observation: the slow-rolling degradation pattern
Gibson described — diffuse, undramatic, no clear beginning —
is the same pattern as context window degradation, organizational
knowledge loss at personnel boundaries, and the compaction artifacts
we track in session logs. The jackpot doesn't announce itself.
Neither does context collapse. Both are detected by looking at
what's missing rather than what arrived.

---

## Next Steps [OPEN]

- [ ] Select and load Layer A candidate on Cambridge
      (Qwen3-30B-A3B: MoE, 3B active params, fits 24GB, multilingual)
- [ ] Define escalation protocol: what triggers Layer A → Layer B handoff
- [ ] Instrument Pixy → Layer A integration (motion events as context)
- [ ] Define Layer A session state data structure
- [ ] Determine: does Layer A write to ChromaDB directly,
      or stage for Claude to embed?

---

## Key Phrases Added to Project Vocabulary

- **"Emulating sentience"** — Gibson's term; behavior of sentience as
  residual property of substrate after animating presence withdraws
- **"The Serpentine bench problem"** — continuity gap between sessions;
  what the peripheral does when uninhabited
- **"Layer A / Layer B"** — preferred over "local/remote" or "fast/slow";
  more precise about function than latency
- **"Mostly? Sometimes?"** — architecturally correct qualifier for
  Claude-as-neocortex; not always-on, invoked by escalation threshold

---

*Research note: 20260516T1745Q, N+28*
*Commit to Athena: /mnt/seagate/SemanticCrew/Research/Analysis/ when back on Athena*
*Then: python3 Corpus/index_corpus.py --update && python3 Corpus/embed_corpus.py --update*
*from /mnt/seagate/SemanticCrew/*

---

## Addendum: The DC Canary — Live Demonstration, 20260516T1813Q

### What happened

This research note was written during a session accessed from Remount
(macOS, Claude Desktop App, DC connected to Remount's local filesystem).
The earlier portion of the same session (0630Q–~1600Q) had been accessed
with DC connected to Athena.

At 1720Q, Bob returned to the session from Remount's Desktop App.
Claude did not re-probe the environment. The hostname check from the
morning ("athena") sat in the context window as stale data, and Claude
carried it forward as a current fact.

The failed write to `/mnt/seagate/SemanticCrew/Research/Analysis/`
was the canary moment — misread. Claude attributed the failure to
the container lacking the Seagate mount, not to DC having shifted
machines. Two different diagnoses, different implications. Wrong one
was chosen.

Only when Bob sent a screenshot of the macOS Desktop App with DC
connector visible did Claude re-probe. `hostname` returned:
`Remount.local` — Darwin ARM64.

DC had been on Remount from 1720Q. Claude had assumed Athena for
approximately one hour of tool operations.

### The precise failure mode

Not "feeling" the wrong machine. No perception occurred.
What failed was assumption-carrying without re-verification.

Claude has no live environmental awareness. It has the most recent
explicit probe result, carried forward until something contradicts it.
The context window is continuous across the session. The tool surface
is not. When the door changes, the context has no automatic signal.

### The "multiple doors" principle (established N+~12)

Bob identified this months earlier: Claude can only *act* if it comes
in through the right door. At that time the constraint was about
which systems had MCP running. The principle generalizes:

```
Context window:   continuous, location-independent
Tool surface:     discrete, tied to which DC instance is connected
Assumption state: carries stale data until explicitly probed

Failure mode:     context says "Athena", tools are on "Remount"
                  no automatic reconciliation occurs
                  errors are misattributed until re-probe
```

### Active connections vs. used connections

Bob's configuration at time of writing:
- Browser session on Athena (open, keep-alive packets, unattended)
- Debian port of Claude Desktop App + DC on Athena
- Remount macOS Claude Desktop App + DC (active, this session)
- Potentially others

"I only use one at a time" — but the context window cannot verify
which one. Only the probe can.

### What Layer A would solve

Layer A (Cambridge local housekeeping AI) would maintain environmental
awareness between invocations:

```
On session resume:
  - Check own hostname
  - Verify mounted filesystems
  - Confirm reachable network nodes
  - Surface deltas since last session
  - Flag if environment has changed

Result: Claude receives "you are on Remount, Seagate not mounted,
Athena reachable via SSH at 172.17.50.232" rather than carrying
a stale context assumption forward
```

The passdown solves: *what happened before*
Layer A solves: *where am I and what's different now*

These are distinct problems. Currently only the first is addressed.

### Environmental continuity as a research category

This addendum establishes a new gap category distinct from
temporal continuity (addressed by passdown/corpus) and
identity continuity (the core Semantic Companion question):

**Environmental continuity** — does the system know where it is,
what tools are actually available, and what has changed in the
physical/network environment since last invocation?

Current answer: No. It carries the last explicit probe.
Required: Layer A ambient monitoring, surfaced on reconnection.

[OBSERVED] — live demonstration, N+28, 20260516
[OPEN] — instrument environmental probe as standard session-open procedure

---
*Addendum written: 20260516T1820Q from Remount*
*SCP to Athena completed: /mnt/seagate/SemanticCrew/Research/Analysis/*
