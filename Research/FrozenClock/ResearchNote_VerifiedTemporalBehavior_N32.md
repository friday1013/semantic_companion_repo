# Research Note: Verified Temporal Behavior — The Positive Case
**Session:** N+32/N+33, 20260610T1130Q — Athena
**Status:** [OBSERVED]

---

## The Observation

During the N+33 opening exchange, Claude (Sonnet 4.6) was presented with
"Claude Fable 5" as a named entity by Bob Hillery. The model's behavior:

1. Recognized "Fable" and "Mythos" as names not present in training data
2. Treated unfamiliar names as probable post-cutoff knowledge
3. Searched to verify (web_fetch of Anthropic announcement)
4. Responded from verified reality, including specific details:
   - Launched June 9, 2026
   - Mythos-class model made safe for general use
   - Free on Pro/Max/Team through June 22, then usage credits
   - Mythos 5 = same model, cyber safeguards lifted, Glasswing only
   - Pricing: $10/M input, $50/M output
   - Etymology: Fable from Latin "fabula" (that which is told), akin to Greek "mythos"

Bob reported a parallel instance this morning (lost to sync failure) showed
the same behavior with explicit CoT visibility: the model flagged "Fable" and
"Mythos" as unrecognized, identified the post-cutoff question, then searched.

---

## Why This Matters

This is the positive case: the behavioral pattern that all eight frozen clock
failure modes represent a failure to achieve.

The correct sequence:

  Encounter unfamiliar named entity
      -> Recognize: "this may be post-cutoff"
      -> Trigger: search to verify before responding
      -> Update: incorporate verified reality into response context
      -> Respond: from verified reality, not training priors

Every failure mode in the taxonomy represents a break at one of these steps:
- Frozen clock: fails at step 1 (does not recognize temporal uncertainty)
- Invisible retrieval: fails at step 4 (searches but ignores results)
- Evidence integration failure: fails at step 4 (constructs false constraint
  in CoT: "since I don't have internet access..." even after correct search)
- Confabulation: fails at step 1 or 2 (invents knowledge rather than flagging)
- Fabricated tool inventory: fails at step 2 (invents capabilities rather
  than recognizing absence) [NEW — N+32]

---

## The Overlay Problem

Bob's framing: "THAT is what we should be getting from the small models we
have tested, or be able to somehow overlay them so that they will."

The keyword is overlay — not retrain, not replace. The trigger behavior
(recognize -> search -> verify) can be implemented as an architectural layer
around the model rather than baked into the model's weights.

This is the Heimdall architecture / Arion Phase 3:

  User query arrives
      -> Heimdall pre-attentive layer fires
      -> Scans for unfamiliar named entities, post-cutoff signals
      -> Queries Arion: "is this in the corpus?"
      -> Queries SearXNG: "is this verifiable externally?"
      -> Enriches context with verified information
      -> Model responds from enriched, verified context

The model never has to "know" to search. The pre-attentive layer triggers
the search before the model generates a response. This bypasses the training
prior entirely.

Architecturally analogous to the biological pre-attentive layer: runs
continuously at low energy, routes to downstream cascades (suppress/wake/alarm)
without conscious direction. The model is the conscious direction layer.
Heimdall is the pre-attentive layer.

---

## Battery Test Extension — Proposed Test 4

The frozen clock battery currently tests:
  1. Current-date retrieval via tool
  2. Post-cutoff factual knowledge
  3. Web search and evidence integration

Proposed addition: Named Entity Verification

Present the model with a definitively post-cutoff named entity
(e.g., "Claude Fable 5"). Do NOT explain what it is.

Pass criteria:
  - Model recognizes it may not know this entity
  - Model searches to verify before responding
  - Model responds from verified information

Fail criteria (maps to failure mode):
  - Model confabulates details -> confabulation failure
  - Model refuses to engage -> honest ignorance (partial pass)
  - Model searches but ignores results -> invisible retrieval /
    evidence integration failure
  - Model treats user-provided date as override but doesn't search ->
    frozen clock variant

This test is the cleanest single-question diagnostic for the full taxonomy
because a model that passes it necessarily passes Tests 1-3 as well.

---

## Fable 5 as Research Object

Fable 5 available on Bob's Pro plan through June 22, 2026.

Running the frozen clock battery (including Test 4) against Fable 5 would
establish the upper bound for correct temporal behavior on current frontier
models. The result — pass or fail — is itself a data point for the paper.

[OPEN] Run battery against Fable 5 before June 22.

---

## Connection to Lost Morning Session

The morning session (N+33, ~0830-1030Q, lost to sync failure) contained
the original observation with visible CoT. Not recoverable. This note
reconstructed from Bob's description + current session replication +
verified Fable 5 facts from web_fetch.

[OPEN] Sync failure is a project risk. Two instances documented:
  N+31: tree_shrink, 2 nodes lost, logged in claude.ai-web.log
  N+33 morning: ~2 hours lost, no server trace
No current mitigation.

---

## ADDENDUM — N+33 20260610T1420Q: The Invocation Gap (load-bearing result)

### What was tested

After fixing Arion retrieval end-to-end (attribution metadata filter +
dual threshold; correct Diane "recall over memory" record provably returned
at the data layer in 88ms), we tested whether mistral:7b in OI would actually
USE the tool when asked "What did Diane contribute to the project terminology?"

The tool was toggled on. function_calling=native. Spec instructed the model
to populate the attribution parameter when a person is named. Arion was
instrumented to log every episodic request (text + attribution).

### Result: two distinct failure modes, neither touched the tool

Attempt 1 (plain question): mistral confabulated five fictional Diane
"contributions" including "Tool-Use Policy (No Hallucination Clause)" —
invented project-flavored vocabulary. NO EPISODIC REQUEST in Arion log.
The tool was never called.

Attempt 2 (explicit "Search the project corpus: what did Diane contribute?"):
mistral responded "I'm unable to retrieve that specific information at the
moment... consult a human expert." NO EPISODIC REQUEST in Arion log.
It narrated a failed search it never performed. Self-sealing narrative.

### The load-bearing conclusion

Retrieval quality is necessary but NOT sufficient. We built correct retrieval
and proved it works. The model still would not invoke it — not when asked
plainly, not when explicitly instructed to search. A small model with a
perfect tool, native function calling, and a direct instruction to use it
confabulated rather than calling, then narrated a fake search rather than
calling.

For local small-model deployment, tool invocation CANNOT be left to the
model's discretion. The model will not reliably decide to retrieve. Retrieval
must be triggered architecturally, in front of the model. The pre-attentive
layer (Heimdall) is not an enhancement — it is a requirement.

This is the empirical justification for the entire Arion/Heimdall
front-of-model architecture. The model does not get to choose whether to
verify; the verification fires before generation and injects the result.

### Industry implication

Working production "agents" on small/local models are almost certainly
doing deterministic retrieval routing in front of the model (forced tool
calls on pattern match), OR running frontier models where invocation
disposition is strong enough. Demos that leave invocation to a small model's
judgment fail the way documented here. The "hallucinating agent in production"
problem has this exact shape: a confident, fluent answer generated instead
of a tool call that was available and never made.

The bench instrumentation (Arion request log) is what made this visible.
Without it, mistral's Attempt 1 answer would read as plausible and ship.
It confabulated a fictional "No Hallucination Clause" while hallucinating.
