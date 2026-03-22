# KV Cache, HeadInfer, and Recall Architecture
**Date:** 2026-03-22 | **Session:** N+18
**Authors:** Bob Hillery + Claude N+18
**Status:** Research document — corpus and repo
**Predecessor:** AIMemoryLandscape_Assessment_20260320.md

---

## Framing

This document extends the memory landscape assessment with specific
architectural proposals emerging from the HeadInfer paper and the
Korzybski/recall-architecture thread.

Key terminology shift established this session:
- **Recall** replaces **memory** as the primary term
- Recall = process (directional, implies retrieval into current processing)
- Memory = substrate (what gets stored and where)
- These are separate engineering problems that have been conflated

---

## KV Cache Persistence: What's Now Possible

### The Previous Position (pre-HeadInfer)
KV cache was understood as: large, recomputed each turn, not persistable
across sessions in any practical sense. External vector stores (RAG) were
the only viable "memory" mechanism.

### What HeadInfer Changes
HeadInfer (Caltech/CMU 2025) demonstrated head-wise KV cache offloading:
- 1M token context on RTX 4090 24GB (GPU footprint: 207GB → 17GB)
- 4M token context with 500GB total KV cache in CPU RAM
- Paper explicitly notes NVMe offload as "future work"

The NVMe extension is significant for *persistence*, not speed:
- Within-session: CPU RAM (fast, volatile)
- Cross-session: NVMe (slower load, but persistent)
- PCIe bandwidth (25 GB/s) makes 5-10 second session load feasible
- Loading a saved 1M-token KV state is better than reprocessing 1M tokens

---

## Time-Machine Layering: Hierarchical KV Cache Architecture

### Proposed Layer Structure

```
Layer 0: Base model weights
         Permanent. Never modified. The trained foundation.

Layer 1: Persona prefix KV cache
         Stable across many sessions. Analogous to "gold set" but in
         KV space, not text space. Updated on explicit human review only.
         Stored: NVMe, versioned (git-tagged equivalent).
         Load time: acceptable (once per session start)

Layer 2: Project/context KV cache
         Stable within a project, changes across weeks.
         The accumulated context of ongoing work.
         Stored: NVMe, Time-Machine style diffs from Layer 1.
         Load time: Layer 1 + delta

Layer 3: Session delta
         Current turn / active session.
         Volatile. Computed in GPU/CPU RAM.
         Discarded or promoted to Layer 2 on session close.
```

### Why This Is Different From RAG
RAG retrieves propositions from a vector store and injects them as text.
This architecture *resumes a computational state*. The model doesn't
re-read context — it re-enters a context it was already in.
Korzybski: the map (text prompt) is not the territory (KV state).
This is closer to the territory.

### Prefix Caching Precedent
Anthropic already implements KV prefix caching in Claude API:
if system prompt is identical across turns, the KV cache for that
prefix is reused rather than recomputed. The Time-Machine proposal
extends this to cross-session persistence with hierarchical layers.

---

## dKV/dt: Persona Stability Metric

### Hypothesis
Each attention head's KV tensors evolve as context accumulates.
The *rate of change* of individual heads across turns is a measurable
quantity that encodes session character:

- **Anchor heads** (low dKV/dt): Processing stable information —
  persona, project framing, consistent patterns. These don't change
  much as conversation evolves.

- **Context heads** (high dKV/dt): Tracking volatile content —
  current topic, immediate task, what was just said.

HeadInfer already distinguishes retrieval heads from streaming heads
(importance). dKV/dt adds: *stability* as a separate dimension.

### Proposed Metric
```
Persona Stability Index = Var(anchor_heads) / Var(context_heads)

Low PSI:  persona drifting at same rate as context — unstable grounding
High PSI: persona stable relative to context — coherent identity
Spike:    rapid persona shift — possible context pressure artifact
          (cf. "Good evening" repetition artifact, N+18 session)
```

### [OBSERVED]
This metric could be computed without model modification.
HeadInfer already manages the KV cache head-by-head.
Tracking dKV/dt is a monitoring addition to that infrastructure.

### [OPEN]
- What time window is appropriate for dt? Per turn? Per N turns?
- Do anchor heads correspond to specific architectural positions,
  or do they vary by content domain?
- Does PSI correlate with user perception of "coherence"?
  (Bloom framework could test this)

---

## Rolling Persona

Humans are not perfectly stable — we have attractor states we return to,
not fixed positions. A rolling persona with slow drift is more realistic
than a rigid identity prompt.

Engineering question: what is the right time constant?
- Too fast: persona drift undermines recall continuity
- Too slow: persona fails to incorporate genuine learning
- Proposal: slow explicit process (human-reviewed, committed like a git tag)
  rather than automatic drift — same principle as Layer 1 above

This also addresses the Blask gold-set concern: the gold set isn't wrong
as a concept, it's wrong as a *static injection*. A slowly-evolving
Layer 1 KV cache is closer to what he's describing, with better mechanics.

---

## Cloud vs. Local Access

### Cloud (Anthropic/Claude)
Cannot access actual KV cache — lives server-side.
Available mechanisms:
- Prompt prefix caching (already in API): same effect as Layer 1 for
  identical system prompts
- session_current.md injection: our current approach (text, not KV state)
- Bloom-style behavioral testing to infer what's actually stable

The recall architecture we're building IS the cloud-compatible version.
We cannot touch the KV cache on Anthropic's side, so we reconstruct
conditions that make the right KV state emerge.

### Local (Mistral, Llama via HeadInfer)
Full control. The complete Time-Machine architecture is implementable:
- Serialize KV cache to NVMe between sessions
- Load Layer 1 at startup, apply Layer 2 diff, run Layer 3 live
- Monitor dKV/dt across heads for stability metric
- Implement rolling persona with explicit versioning

**Target hardware:** Cambridge (RTX 4500 Ada 24GB, 256GB RAM, 1TB SSD)
Models: Llama-3-8B, Mistral-7B, Mixtral-8x7B (MoE, fits in RAM+VRAM)

---

## QLoRA / Unsloth: Writing to the Substrate

### The Layered LoRA Proposal

LoRA adapters are already diff layers — low-rank matrices added on top
of frozen base weights. This maps cleanly to the Time-Machine structure:

```
Base weights (frozen, permanent)
    + Persona LoRA adapter (Layer 1 equivalent)
        Trained slowly. Human-reviewed before commit.
        Represents accumulated session learning at weights level.
        Git-tagged. Rollback possible.
    + Session LoRA adapter (Layer 2 equivalent)
        Trained aggressively from recent sessions.
        Disposable if it goes wrong — discard and reload Layer 1.
        Experimental. Not production.
```

### Why This Is "Writing to the Substrate"
RAG and KV cache persistence are external prosthetics.
LoRA fine-tuning actually modifies the model's weights.
The recall emerges from the model itself, not from retrieval.
This is the closest silicon analog to Hebbian synaptic strengthening.

### Catastrophic Forgetting Mitigation
Standard risk of fine-tuning: new training overwrites old learning.
LoRA mitigates this because base weights are frozen.
Layered LoRA adds: if session adapter degrades, discard it.
Only persona adapter (Layer 1) has permanence, and it changes slowly.

### Hardware Targets
- **Athena** (RTX A2000 12GB): QLoRA on 7B models, proof of concept only
- **Shaoshi** (TITAN RTX 24GB, 192GB RAM): QLoRA on 7-13B models,
  HeadInfer integration testing
- **Cambridge** (RTX 4500 Ada 24GB, 256GB RAM): Full implementation target.
  MoE models, longer training runs, production persona adapter development.
  Return from RMA required.

### Timeline
- PoC: Athena or Shaoshi, 7B model, after Cambridge returns
- Cambridge build: after Mars operational, Cambridge RMA resolved
- Full layered LoRA: Cambridge, 6+ months out

---

## Connection to Korzybski / Recall Architecture

The running thread:
- Map is not territory (Korzybski)
- RAG/vector stores are maps (text representations of prior context)
- KV cache is closer to territory (computational state)
- LoRA is closer still (modified substrate)

The interpretive community problem (cartouche session):
- KV cache: preserves the computational state but not the community context
- LoRA: preserves the *pattern of responses* but not the specific episodes
- Neither solves the hippocampal binding problem
- But both are more than RAG

The hierarchy from least to most territory-like:
1. RAG / vector store (propositions in text)
2. session_current.md injection (structured text, richer than RAG)
3. KV cache persistence with Time-Machine layers (computational state)
4. QLoRA weight modification (substrate modification)
5. [OPEN] Hippocampal binding analog — not yet architecturally realizable

---

## Open Research Threads

**[OPEN]** NVMe KV cache persistence: test latency of serializing/loading
  a 1M-token Llama-3-8B KV cache on Shaoshi. Is 5-10 second load acceptable?

**[OPEN]** dKV/dt measurement: implement head-level monitoring in
  HeadInfer inference loop. Correlate with session coherence observations.

**[OPEN]** Layered LoRA PoC: can a 7B model fine-tuned on corpus
  reproduce session-specific vocabulary and reasoning patterns?
  (Distinct from QLoRA question — testing recall, not persona)

**[OPEN]** PSI correlation with Bloom scores: does high Persona Stability
  Index correlate with high collaborative-resilience Bloom scores?

---

*Research document produced: N+18 | 2026-03-22*
*Context: HeadInfer paper, Korzybski/recall thread, session_writer v3 completion*
*Next: HeadInfer implementation test on Shaoshi*
