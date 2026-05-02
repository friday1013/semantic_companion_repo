# Memory Architecture: Joint Synthesis
## Claude N+24 + Kusanagi, 20260502
Contributors: Bob Hillery, Claude N+24, Kusanagi
Tags: memory-architecture synthesis episodic semantic procedural consolidation pre-attentive

## The Load-Bearing Problem

Bob Hillery: The BIG challenge is real memory, not look-up tables.

Kusanagi: Storage is not memory. Retrieval is not remembering.
Memory begins when stored episodes can be promoted into abstractions
and procedures that change future behavior.

Rate-limiting constraint (Bob Hillery 20260502): Full context ingestion is O(n).
Semantic retrieval is O(log n) -- but only if the right cue fires retrieval.
The overhead becomes the rate-limiting asymptote.
The solution is not bigger context. It is smarter triggering.

## The Four Memory Tiers (Kusanagi, confirmed N+24)

WORKING MEMORY
What is live right now. Context window plus short-lived scratch state.
Schema: session_id, active_goal, current_entities, open_threads,
  recent_tool_results, active_constraints, scratch_hypotheses, expiry_time

EPISODIC MEMORY
Timestamped events with provenance. Specific events in space and time.
Schema: event_id, timestamp, type, source, actors, entities, summary,
  raw_pointer, embedding, salience_score, trust_score, novelty_score,
  linked_goals, linked_events, promotion_state

SEMANTIC MEMORY
Compressed abstractions from repeated episodes.
Not I saw this once but this pattern tends to mean X.
Schema: concept_id, statement, confidence, provenance_bundle,
  support_count, contradiction_count, last_validated, related_concepts,
  domain_tags, supersedes, superseded_by

PROCEDURAL MEMORY
Callable routines. Machine analogue of muscle memory.
Bob Hillery classroom exercise: stand_up() assumed balance() which assumed
  vestibular_input() -- the programmer did not know those subroutines existed.
Schema: procedure_id, name, trigger_conditions, preconditions,
  steps_or_callable_modules, expected_outputs, rollback_conditions,
  success_metrics, reliability_score, last_run, provenance, version

## The Shared Representational Currency (Claude N+24)

Each module converts domain-specific output into common currency
at its output boundary. Everything above is ignorant of below.

  Vision:      pixels         -> structured text (objects, positions, changes)
  Audio:       waveform       -> structured text (words, tone, salience)
  Pulse:       system metrics -> structured text (status, anomalies, load)
  Temperature: sensor data    -> structured text (state, trend, alert)
  Capture:     raw events     -> structured event schema

The supervisory model never sees pixels, waveforms, or raw sensor data.
This is how V1 works: sends edges and motion vectors, not photoreceptor data.

OPEN: Minimal viable schema for the currency needs specification.

## The Abstraction Layer (Claude N+24, CP/M frame)

Kildalls CP/M BIOS sat between hardware and application programs.
Programs called the abstraction; the abstraction translated.
Our requirement: thin translation layer between sensors and shared substrate.

OPEN: What does our BIOS look like exactly? Next design question.

## The Pre-Attentive Trigger Layer (Claude N+24)

Kusanagi handles retrieval once triggered.
It does not answer: what does the triggering?

Sleep-auditory parallel (Bob Hillery 20260430): auditory system during sleep
runs continuously at low energy, applies weighted evaluation, fires escalation
only when salience exceeds threshold.
Three categories: suppress, wake, alarm -- different downstream cascades each.

Required properties: low energy, always-on, evaluative not just amplitude,
  pre-generative (operates before the token stream begins).

Current gap: session_writer instruments session-close and significance thresholds.
Pre-attentive trigger needs response-initiation level granularity or continuous.

## The Disambiguation Layer (Claude N+24, 20260502)

Compressed stimulus returns a CANDIDATE SET requiring disambiguation
against current context -- not a single memory.

Example: Claude activates {N+24, Shannon, Debussy, ...}
Current context does the disambiguation. Shannon loses top slot but his
neighborhood (entropy, channel capacity, information theory) remains activated.

ChromaDB nearest-neighbors IS the candidate set.
The LLM IS the disambiguation layer.
We have the rough shape. We lack the trigger.

## Promotion Rules (Kusanagi)

Episode -> Semantic when:
  same pattern in multiple episodes, provenance strong, contradiction rate low

Episode -> Procedural when:
  same action sequence succeeds repeatedly, preconditions stable, rollback known

Semantic -> Procedural when:
  semantic rule repeatedly implies stable executable policy, bounded risk

Anything -> Archive/Decay when:
  stale, weak provenance, contradicted, better representation exists

## Retrieval Scoring (Kusanagi)

Weighted blend: semantic relevance + recency + salience + trust/provenance +
  unresolved-thread match + reinforcement from repeated successful use +
  contradiction penalty

Retrieval must be task-shaped, not just nearest vector.

## The Consolidation Daemon (Kusanagi)

Run on Cambridge, NOT inline with conversational shell.
Function: cluster episodes, detect patterns, propose abstractions and procedures,
  merge duplicates, flag contradictions, decay stale items, write audit trail.

Complementary-learning-systems principle:
  fast episodic capture (hippocampal-like) + slower abstraction (neocortical-like)

## Governance Rules

Before promoting: provenance check, contradiction scan, confidence estimate,
  operator approval for high-impact, audit log entry.

Hard rules:
  Do not overwrite attested facts for conversational smoothness.
  Do not silently merge conflicting memories.
  Keep raw pointer to source material. Uncertainty remains explicit.

## Hardware Mapping

Athena (RTX A2000 12GB, 64GB RAM):
  Live shell, working memory, fast episodic capture, primary human interaction

Cambridge (RTX 4500 Ada 24GB, 256GB RAM, 25TB):
  Consolidation daemon, 20B-30B local models, multimodal experiments,
  promotion pipeline, vector stores, reranking, graph storage

Shaoshi (TITAN RTX 24GB, 192GB RAM):
  CAP unchanged, qwdata team storage, potential second serving node

Mars (planned): Huginn/Muninn, background monitoring, orchestration

## Build Order

1. Standardize event schema (shared representational currency)
2. Separate stores: working, episodic, semantic, procedural
3. Implement retrieval scoring beyond embeddings alone
4. Pre-attentive trigger layer (what decides when to query)
5. Build the consolidation daemon on Cambridge
6. Add promotion/demotion audit logs
7. Compile repeated successful workflows into procedures

## The Synthesis in One Sentence

The unsolved problem is not storage. It is selective, cueable, consolidating
memory that can become competence -- triggered pre-attentively, retrieved as
candidate sets, disambiguated in context, and promoted from episodes into
procedures that change future behavior.

## Cross-References

ResearchNote_CommonSubstrate_N24_20260501.md
research_pre_generative_monitoring_20260430.md
KusanagiArchitecture.pdf (/home/hillery/Downloads/)
ClaudeImagesArchitecture.pdf
SemanticPaging_LiveDemo_20260215.md

Joint synthesis by Claude N+24 and Kusanagi
Framing: Bob Hillery, 20260502, SemanticCrew / QuietWire