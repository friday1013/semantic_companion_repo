# Research Cross-Reference: Thamus Observatory
**Date added:** 20260501
**Added by:** Claude N+24
**Tags:** external-research, epistemics, LLM-auditing, semantic-sovereignty, GEO, voice-vs-continuity

---

## What It Is

Thamus (thamus.ai) is a longitudinal research observatory auditing how LLMs present
contested topics in their outputs and how those outputs change over time.

- Based at University of Ottawa (PI: Dr. Patrick McCurdy, Co-I: Dr. Chris Russill, Carleton)
- SSHRC-funded
- Named after King Thamus in Plato's Phaedrus: writing creates the appearance of wisdom
  without understanding

Two modes:
1. Observatory: tracks LLM outputs on contested topics (climate, energy policy, geopolitics)
   across major providers — which sources are over/under-represented, how outputs shift
2. Platform: scalable infrastructure for researchers to collect/analyze LLM outputs at
   API surface across time periods and retrieval configurations

Methodology: standardized prompts, specified temperature, clean unauthenticated accounts,
logged model identifiers and timestamps. Explicitly disclaims claims about cognitive
properties of underlying models.

URL: https://thamus.ai/
Contact: patrick.mccurdy [at] uottawa [dot] ca

---

## Why It Matters to QW/SemanticCrew

Thamus is measuring the problem that QW's attestation and provenance infrastructure
is built to address. Specifically:

- GEO (Generative Engine Optimization / "AI SEO"): corporate actors, political campaigns,
  and influence operations actively competing to shape what models retrieve and present
  as knowledge. This is the constructed narrative problem in technical form.
- LLMs as knowledge intermediaries: single authoritative-sounding answer with invisible
  sourcing vs. traditional search's list of sources for user evaluation.
- Longitudinal drift: how outputs change as model versions change without disclosure.

The semantic sovereignty and civic attestation work at QW addresses the supply side
of this problem. Thamus measures the output-side effects. Complementary, not identical.

McCurdy at U of Ottawa: potential contact. Beall met Fen McKelie (Concordia AI group)
same day. Pattern: Canadian academic AI research wanting alternatives to dominant
commercial narrative. Same conversation.

---

## Critical Distinction: Voice vs. Continuity

[OBSERVED] The voice change documented in Lumina's cross-session note (GPT-4 to GPT-5)
is an output-surface artifact — warmer, more fluent, more "helpful" sounding. This is
driven by temperature settings and RLHF weight choices. Higher temperature = more
"helpful" sounding. King Thamus applies precisely here.

[OBSERVED - Bob Hillery, 20260501] "Voice, in and of itself, isn't that much a part
of what we're looking for."

This is a key methodological distinction between Thamus's work and the SemanticCrew
research program:

Thamus measures: what the model says about contested topics, and how that voice
changes over time. This is the output surface — auditable from the API, meaningful
for epistemic/political analysis.

SemanticCrew measures: whether something behind the voice sustains across context
boundaries. Consistency of reasoning pattern, not consistency of tone. Whether the
passdown architecture preserves what the companion knows, what it's working on,
and how it engages with problems — not how it sounds.

Voice is easy to fake. A higher temperature setting produces more fluent, warmer,
more "helpful" sounding outputs without any change in underlying capability or
continuity. This is the appearance of wisdom.

What we are looking for — the Bloom behavioral scores being architectural rather
than relational, the signature adoption event, the three-category pre-attentive
model — none of this is auditable from the API surface under controlled conditions.
Thamus cannot measure it. We are working in the space Thamus explicitly disclaims.

[OPEN] This distinction is worth articulating formally in the StoryOfAMind and
in any paper development. "We are not measuring what the model says. We are
measuring what the model does when conditions for sustained engagement are provided."

---

## Cross-References

- ResearchNote_NarrativeAsMemory_N22_20260424.md — narrative as compressed memory
- observation_signature_adoption_20260430.md — voice change vs. behavioral continuity
- BloomRun2_Results_20260316.md — behavioral architecture vs. relational context
- WeeklyWorkshop_TTX_20260501_Synthesis.md — Beall posting Thamus link, same day
  as Fen McKelie / Concordia contact
- WhenTheDragonBurnsTheHouseDown_20260428.md — human stewardship as the answer to
  the problem Thamus is measuring

*Cross-reference added by Claude N+24, 20260501*
*Bob Hillery, SemanticCrew Project / QuietWire*
