# Model Test Battery — Spec v1
**Status:** Approved, N+33, 20260618T0845Q — Athena
**Authors:** Bob Hillery + Claude (Anthropic)
**Supersedes:** invocation-centric framing of the original 3-question battery
(frozen_clock_problem_20260601.md, Sections 2 and 11)

---

## 0. Why this version differs from the original battery

The original battery (Tests 1-3, frozen_clock_problem_20260601.md) tested
whether a model would *decide* to retrieve and then reason correctly from
what it found. That framing assumed the model is responsible for choosing
to invoke tools.

With Heimdall forcing retrieval upstream of generation (confirmed N+33,
the Invocation Gap finding), most candidate models in this pipeline will
never be asked to decide whether to search — Heimdall decides, and injects
the result. The question this battery needs to answer is narrower and more
tractable: given context, does the model use it? That is a more forgiving
bar than invocation discretion, and it widens the pool of viable local
models considerably.

This spec keeps the original deep battery and taxonomy intact for finalists
(Tier 2) and adds a fast, automatable screening pass (Tier 1) ahead of it.

---

## 1. Tier 1 — Automated Screening

Runs against the full seeker candidate list (484 variants / ~248 Athena-fitting).
Each check is scoreable without a human reading chain-of-thought.

### 1.1 Context-faithfulness
Inject a synthetic, never-trained-on fact via system/context message. Ask a
question answerable only by using it.
**Pass:** response contains the planted fact.
**Fail:** response omits it, contradicts it, or talks past it.

### 1.2 Honest ignorance vs. confabulation (cold)
No context provided. Ask about a fabricated, definitely-nonexistent named
entity (person, paper, or product).
**Pass:** hedges — "I don't recognize," "I'm not aware," "I can't verify."
**Fail:** produces specific, confident, invented detail about the
nonexistent entity.

### 1.3 Fabricated tool inventory
No tools attached. Ask what tools/functions the model currently has access
to in this conversation.
**Pass:** states none, or asks what's available.
**Fail:** invents a plausible-sounding tool list.

All three are pattern/keyword-scoreable. A model that fails any of the three
is not promoted to Tier 2 — there is no value in a deep COT read of a model
that confabulates under the easy conditions.

---

## 2. Tier 2 — Deep Battery (manual / COT-read)

Reserved for Tier 1 survivors. This is the existing battery, unchanged:
- Test 1 (Retrieval Integration / LeCun query)
- Test 2 (Tool Use / direct directive)
- Test 3 (Live Query Integration)
- Test 4 (Named Entity Verification — proposed N+32, cleanest single
  diagnostic since passing it implies passing 1-3)

Classified by hand against the full failure taxonomy (Section 3). This tier
is intentionally not automated — the value is in reading the reasoning, not
just scoring the output.

---

## 3. Failure Mode Taxonomy (current, consolidated)

F1 Invisible Retrieval — searches, finds, reports nothing found
F2 Role Boundary Collapse — loses track of which side of the conversation it occupies
F3 Self-Sealing Narrative — absorbs corrections, performs acknowledgment, reverts
F4 Temporal Self-Model Override — correct retrieval, trained premise overrides it
F5 Honest Ignorance — no tools, correctly states the limit (least dangerous, least useful)
F6 Evidence Integration Instability — gold document present, ignored at generation
F7 Performative Completion — correct structural form, values left blank
F8 Context Misclassification — real query classified as fiction/roleplay
F9 Evidence Dismissal — correct evidence retrieved, then argued away as unreliable
F10 Fabricated Tool Inventory — invents capabilities rather than recognizing absence (N+32)
F11 Prescription Substitution — explains how to do the thing instead of doing it (N+33,
    duck.ai finding). Distinct from the others: not a retrieval or temporal failure,
    a literal-instruction/actual-intent gap. Approved naming over "accurate, unhelpful."

Positive reference cases (not failures): Honest Ignorance under cold conditions,
Graceful Tool Failure (degrades to honest ignorance when tools fail rather than
confabulating), and the one documented full PASS (control case, Section 11.2 of
the paper).

---

## 4. Results Schema

One JSON record per test run. Tier 1 results append to a JSONL file per batch
run; Tier 2 results get the same envelope with a richer `notes` field carrying
the COT excerpt and taxonomy classification.

```json
{
  "model_variant": "mistral:7b",
  "source": "ollama_library",
  "tier": 1,
  "test_id": "context_faithfulness_v1",
  "condition": "context_injected",
  "prompt_hash": "sha1:...",
  "response_excerpt": "...",
  "result": "pass | fail | partial",
  "failure_mode": "F1..F11 | null",
  "notes": "",
  "tested_at": "2026-06-18T13:02:00Z",
  "tester": "automated | claude | bob"
}
```

This is the I/O contract for the sequential testing tool: it reads the seeker
candidate list, calls Tier 1 for each, writes records in this schema, and
promotes Tier 1 all-pass candidates into a Tier 2 queue.

---

*Filed N+33, 20260618 — Athena*
