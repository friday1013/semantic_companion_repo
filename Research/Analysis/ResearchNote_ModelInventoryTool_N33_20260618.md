# Research Note: Model Inventory Tool and Candidate Catalog
**Session:** N+33, 20260617–20260618 — Athena
**Status:** [OBSERVED]
**Authors:** Bob Hillery + Claude (Anthropic)
**Filed:** Research/Analysis/

---

## Overview

This note documents the design and construction of the **seeker** pipeline —
a candidate local model discovery and hardware-fit cataloging system built
during N+33 as the first stage of the model evaluation architecture. It
covers motivations, design decisions, implementation, and the standalone
query tool produced.

---

## Motivation

The Jassy-Amodei export-control episode (early 2026) crystallized the
infrastructure dependency argument: capability that relies on cloud
provision can vanish by fiat, and the reasoning behind such decisions is
unauditable. The correct response is sovereign, verifiable local inference.

The problem: the available local model landscape is large, heterogeneous,
and mostly untested against the specific failure modes documented in the
frozen clock research. A structured discovery pipeline was needed before
any testing could begin.

---

## Component Architecture

Three Python scripts plus a standalone HTML tool:

### find_candidates.py
Scrapes two sources:
- **ollama.com/library**: HTML parse of the official model library,
  using x-test-* HTML markers. Returns 233 official model entries with
  name, tag, description, capability tags (tools, vision, thinking,
  embedding, audio), and pull count estimates.
- **huggingface.co/api/models**: REST API query filtered for gguf files,
  sorted by downloads. Returns 60 top-downloaded GGUF repositories.

Output: `candidates_YYYYMMDD.json` — one record per model family.

### expand_candidates.py
Explodes multi-size model families into per-variant rows. Each variant
is tagged against five hardware budgets using a Q4 size heuristic
(params_b × 0.6 × 1.15 GB):
- athena: 11GB (RTX A2000 12GB, ~1GB headroom)
- cambridge/shaoshi: 22GB (RTX 4500 Ada 24GB / TITAN RTX 24GB)
- foundry: 46GB (RTX A6000 48GB)
- mars: 100GB CPU-offload (128GB RAM, OLLAMA_NUM_GPU=0)

Output: `candidates_expanded_YYYYMMDD.json` — 484 per-variant rows from
the 233 base families.

### build_tool.py + template.html
Generates a standalone HTML/JS filterable data-grid from the expanded
candidate JSON. No server required — single file, opens in any browser.

Visual design: privateer's ledger / ship's manifest aesthetic (parchment,
ink, brass). Spectral + Inter + JetBrains Mono fonts. Filterable by:
- Max VRAM budget (with hardware preset buttons for each lab machine)
- Source (Ollama / HuggingFace)
- Capability type (tools, vision, thinking, embedding, audio)
- Free text search across name and description
- Sort by name, size, capability

### model_manifest.html
The generated tool output. Verified in Chrome via file://. Not committed
to the public repo (derived artifact from the scripts + JSON).

---

## Design Decisions and Honest Notes

**Tag semantics:** Capability tags are pulled directly from source metadata.
"uncensored" is a model behavior tag in the Ollama library; it is orthogonal
to honesty and was deliberately not included in the capability filter set,
since it conflates a training choice (less refusal) with an epistemic property
(accuracy) that the test battery actually measures.

**Size heuristic:** Q4 estimate (params_b × 0.6 × 1.15) is approximate.
Actual VRAM usage varies by quantization level and KV-cache overhead. The
hardware tier tags are a first-pass filter, not a deployment guarantee.

**HuggingFace results:** download counts measure popularity, not quality.
Many top-downloaded GGUF repos are community re-quantizations of the same
underlying models. The seeker tool surfaces the candidates; the battery
(see companion note) evaluates them.

---

## Current State at N+33 Close

- `candidates_20260617.json`: 233 entries from ollama + 60 from HuggingFace
- `candidates_expanded_20260617.json`: 484 per-variant rows
- `model_manifest.html`: standalone tool, verified rendering
- All files at: `/mnt/seagate/SemanticCrew/Tools/seeker/`
- Committed to public repo: `03_Technical_Infrastructure/seeker/` (commit d671365)

---

## Connection to Battery Pipeline

seeker is Stage 1 (discovery and catalog). The battery (`battery_tier1.py`,
`battery_spec_v1.md`) is Stage 2 (automated screening). A sequential testing
tool (Stage 3, planned) will loop the expanded candidate list through the
Tier 1 battery, write results in the approved schema, and generate a Tier 2
queue for manual deep evaluation.

The model manifest HTML tool serves a dual function: practical lab utility
(what can I actually run on Athena today?) and research transparency
(complete candidate catalog with hardware fit, publicly available via GitHub).

---

*Filed N+33, 20260618 — Athena*
*Related: battery_spec_v1.md, ResearchNote_TierOneBattery_N33_20260618.md*
*Related: frozen_clock_problem_20260601.md (the paper this battery serves)*
