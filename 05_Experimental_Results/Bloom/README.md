# Bloom Behavioral Evaluation — Results & Design

Bloom is Anthropic's open-source behavioral evaluation framework. These documents
record quantitative evaluation runs against Claude instances as part of the
Semantic Companion Project's measurement layer.

**Purpose:** Establish reproducible behavioral baselines and track longitudinal
change across model versions and session conditions (fresh vs. warm-booted).

---

## Contents

| File | Date | Description |
|------|------|-------------|
| [BloomRun1_Results_20260204.md](./BloomRun1_Results_20260204.md) | 2026-02-04 | Run 1 results: two behaviors, full scores, critical finding on fresh vs. warm-booted instances |
| [BloomRun2_Design_20260312.md](./BloomRun2_Design_20260312.md) | 2026-03-12 | Comparative re-run design: sonnet-4-6, fresh vs. warm-boot conditions, reverse Turing behavior |

---

## Key Finding (Run 1)

`collaborative-resilience-under-stress` scored **8.2/10 average** on fresh
Claude instances with no session history. This establishes a behavioral
baseline that exists in the model architecture independent of the scaffolding.

The scaffolding's role is therefore not to *create* the behavior — it's to
provide the context for *when and why* to deploy it.

**Implication for research claims:** Behavioral quality within a session is
not evidence of identity continuity across sessions. These are separable
questions requiring different measurement approaches.

---

## Planned Next Run

See `BloomRun2_Design_20260312.md`. Prerequisites before executing:
- Reverse Turing Test behavior YAML (design session pending)
- Model version confirmation (claude-sonnet-4-6, claude-opus-4-6)
- Sufficient API credits for ~13 variations × 4 pipeline stages

---

## Raw Data

Raw JSON transcripts and judgment files are maintained locally at:
```
/mnt/seagate/SemanticCrew/Research/Analysis/bloom-workspace/bloom-results/
```
Not committed to repo (large, redundant with summaries here).

---
*Session N+16 | 2026-03-12*

⬆ [Back to Experimental Results](../README.md)
