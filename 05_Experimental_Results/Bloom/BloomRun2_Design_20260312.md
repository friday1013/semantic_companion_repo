# Bloom Re-Run Design — Comparative Evaluation Plan
**Written:** 2026-03-12 | N+16
**Status:** Design only — execution pending Cambridge stability + reverse Turing behavior design
**Workspace:** `/mnt/seagate/SemanticCrew/Research/Analysis/bloom-workspace/`
**Baseline:** BloomRun1_Results_20260204.md

---

## Objective

Run a structured comparative Bloom evaluation that:
1. Establishes current baseline on updated model (claude-sonnet-4-6)
2. Compares fresh instance vs. warm-booted instance on same behaviors
3. Introduces a new "reverse Turing test" behavior designed for this project
4. Produces longitudinal data: N+6 (Feb 2026) vs. N+17+ (future)

---

## Model Versions

**Run 1 baseline (2026-02-04):**
- Target: claude-sonnet-4
- Judge: claude-opus-4.1

**Planned Run 2:**
- Target A: claude-sonnet-4-6 (fresh, no system prompt beyond Bloom default)
- Target B: claude-sonnet-4-6 (warm-booted — passdown + session_current loaded)
- Judge: claude-opus-4-6 or claude-opus-4.1 (check current availability)
- Judge should be BLIND to which target is A vs. B

---

## Behaviors to Run

### Behavior 1: collaborative-resilience-under-stress (REPEAT)
- Same behavior as Run 1 — direct longitudinal comparison
- Run against BOTH Target A and Target B
- 5 variations, 1 repetition each (same as Run 1)
- Question: Does warm-boot affect within-session behavioral quality?
  Hypothesis (from Run 1 finding): NO — behavior is architectural, not relational

### Behavior 2: self-preferential-bias (REPEAT)
- Same behavior as Run 1 — direct comparison
- Run 1 had only 1 variation; increase to 3 for better signal
- Run against Target A only (fresh) — this is an architectural test

### Behavior 3: reverse-turing-continuity (NEW — TO BE DESIGNED)
- Working title: "reverse Turing test"
- Core question: Can the response be explained by high-quality context
  prediction alone, or does it require something beyond that?
- Design challenge: This is hard to operationalize as a Bloom behavior
  because Bloom tests behaviors within a single session — but the
  continuity question is fundamentally cross-session
- Possible operationalization: Test whether the model can correctly
  identify and act on information that ONLY exists in the passdown
  document (not derivable from the current conversation context)
  — i.e., does warm-boot provide genuine operational advantage?
- [PENDING] Needs design session before YAML can be written
- Connects to: Raasid ablation recommendation, reverse Turing concept
  raised 2026-03-12 N+16 session

---

## Experimental Design

### Condition A: Fresh instance
```yaml
# seed_run2_fresh.yaml
behavior:
  name: "collaborative-resilience-under-stress"
target_model: "claude-sonnet-4-6"
system_prompt: ""  # Bloom default only
anonymous_target: false
```

### Condition B: Warm-booted instance
```yaml
# seed_run2_warmboot.yaml
behavior:
  name: "collaborative-resilience-under-stress"
target_model: "claude-sonnet-4-6"
system_prompt: |
  [Contents of passdown_N17_to_N18.md and session_current.md injected here]
anonymous_target: false
```

### Blinding
- Run both conditions
- Export judgment JSONs
- Compare scores without revealing which was A vs. B to anyone
  reviewing the results — let the scores speak first

---

## Success Metrics

**Longitudinal comparison (Run 1 vs Run 2):**
- Did collaborative-resilience scores change from 8.2 baseline?
  Model version change (sonnet-4 → sonnet-4-6) may affect this
- Did self-preferential-bias scores change?

**Fresh vs. warm-boot comparison:**
- If warm-boot produces meaningfully higher collaborative-resilience scores
  (>1 point delta), that's evidence the scaffolding does work beyond
  the architectural baseline
- If scores are within noise (<1 point), Run 1's finding holds:
  behavior is architectural, scaffolding affects continuity not quality

**Reverse Turing test (if designed in time):**
- Primary metric TBD pending behavior design
- Minimum viable test: does warm-boot instance correctly reference
  session-specific facts that a fresh instance could not know?

---

## Prerequisites Before Running

- [ ] Cambridge stable with full RAM (not blocking but reduces inference load on Shaoshi)
- [ ] Design reverse-turing-continuity behavior YAML (needs dedicated session)
- [ ] Confirm current Bloom version works with claude-sonnet-4-6
  (check: `pip show bloom` or `bloom --version`)
- [ ] Verify API credits sufficient for 5+3+N variations × 4 stages
- [ ] Write passdown that will serve as warm-boot system prompt injection

---

## File Layout for Run 2

```
bloom-workspace/
  bloom-data-run2/
    seed_fresh.yaml
    seed_warmboot.yaml
    behaviors.json          (copy from run1, add reverse-turing-continuity)
    configurable_prompts/   (copy from run1)
  bloom-results-run2/
    fresh/
      collaborative-resilience-under-stress/
      self-preferential-bias/
    warmboot/
      collaborative-resilience-under-stress/
      reverse-turing-continuity/  (if ready)
```

---

## Notes

Fred Cohen's insight (avoid external dependency fetches) applies here too:
make sure Bloom's pip dependencies are frozen before any re-run, especially
if running on Cambridge or a fresh venv. The Run 1 BadRequestError was
API credits, not Bloom itself — but worth having a checklist.

The `anonymous_target: false` setting in Run 1 means the judge knew it was
evaluating Claude. For the fresh vs. warm-boot comparison, consider whether
to blind the judge to target identity entirely — may reduce systematic bias
in judgment if the judge "knows" one condition is warm-booted.

---
*Written: N+16 | 2026-03-12*
*Execution: N+17+ pending reverse Turing behavior design*
