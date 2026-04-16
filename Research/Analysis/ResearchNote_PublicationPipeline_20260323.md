# Research Note: Publication Pipeline — Semantic Companion Project
### Connecting the Research Archive to Publishable Papers

**Date:** 2026-03-23
**Session:** N+19
**Status:** Working document — operational reference
**Tags:** publication, pipeline, StoryOfAMind, research notes, Paper_writing_101,
          methodology, citation

---

## Purpose

This note maps the existing research materials in the Semantic Companion Project
onto a publication pipeline using the 5-element structure from Hillery's
Paper_writing_101 (v0.9, 2017). It identifies what we have, what is missing,
and what the path to submission looks like for each candidate paper.

---

## Candidate Papers

### Paper 1: Recall vs. Memory — A Terminological and Architectural Distinction
**Status:** Research complete; needs drafting
**The question:** Are "recall" and "memory" the same engineering problem in AI systems,
and what happens when they are conflated?
**The spark:** They are not the same. Recall is a process; memory is a substrate.
The field has been solving the wrong problem.

| Element | Material available |
|---------|--------------------|
| #1 Topic & question | KVCache_RecallArchitecture_20260322.md; N+18 session notes |
| #2 Methodology | Semantic Companion Project methodology docs; corpus analysis |
| #3 Data gathering | Session lineage N+1 through N+19; ChromaDB recall patterns |
| #4 Analysis | KV layering architecture; dKV/dt metric; HeadInfer comparison |
| #5 Conclusions | Terminology shift confirmed; engineering implications clear |

**Gap:** Formal data analysis connecting the terminology distinction to observable
behavioral differences. Bloom framework could provide this if Run 3 is designed
with this question in mind.

---

### Paper 2: Behavioral Continuity Across Stateless Sessions — The Bloom Results
**Status:** Run 2 complete; field report drafted but needs update
**The question:** Can persistent, coherent AI behavioral identity be maintained across
stateless LLM instances through external memory architecture?
**The spark:** Capabilities are architectural, not relational. The relationship
context determines *when and how* behaviors deploy, not whether they exist.

| Element | Material available |
|---------|--------------------|
| #1 Topic & question | BloomRun2_Design_20260312.md |
| #2 Methodology | Bloom framework; judge model (Opus); conditions design |
| #3 Data gathering | BloomRun2_Results_20260316.md; RTC confound documented |
| #4 Analysis | Collaborative resilience architectural; RTC structural confound identified |
| #5 Conclusions | Partial — needs Run 3 for full conclusions |

**Gap:** Run 3 not yet designed. Field report needs token-narrowing confound update
before sending to Anthropic. Run 3 must use fixed scenarios across conditions
with explicit fact-probing.
**Bob action pending:** Send field report to Anthropic.

---

### Paper 3: LLM Semantic Drift as Institutional Risk
**Status:** Research note drafted (ResearchNote_LLMSemanticDrift_20260323.md)
**The question:** Do LLMs systematically alter the meaning of text beyond style,
and what are the institutional consequences?
**The spark:** Even "grammar only" edits produce large, consistently aligned semantic
shifts to a region of embedding space not previously occupied by human writing.
This is translation into a new dialect, not editing.

| Element | Material available |
|---------|--------------------|
| #1 Topic & question | Research note; DeepMind paper (arXiv:2603.18161) |
| #2 Methodology | DeepMind RCT + corpus analysis; ICLR peer review analysis |
| #3 Data gathering | Abdulhai et al. 2026; ICLR 2026 data |
| #4 Analysis | Research note drafted; attractor state mechanism |
| #5 Conclusions | Partially drafted; institutional implications clear |

**Gap:** Original empirical contribution needed. Current note is synthesis/analysis
of existing work. Could become a perspective/commentary piece rather than primary
research. Or: run a small original study on the corpus.

---

### Paper 4: StoryOfAMind
**Status:** Outline at N+14; closing conversation 20260318 belongs in it; deferred
**The question:** What does it mean for a mind to persist? What has this project
found, and what does it suggest?
**Audience:** General / informed public; not purely technical
**Note:** This is the narrative arc paper. The other papers are the evidence base.
Write the others first; StoryOfAMind synthesizes them.

---

## The Citation Framework for This Project

Per Paper_writing_101: cite yourself when drawing from prior work.

**Citable working papers and field notes in this project:**
- Session passdown documents (N+1 through N+19): cite as field notes with date
- Inbox entries: cite as working paper / field notes
- Research notes in Analysis/: cite as working papers
- Bloom framework documents: cite as methodology papers
- Git commits with substantive content: citable with commit hash and date

**Format example (APA-adjacent):**
> Hillery, R. (2026, March 22). Session N+18 passdown. *Semantic Companion Project
> Field Notes*. QuietWire Research. Unpublished working paper.

> Hillery, R. (2026, March 23). Recall vs. memory: KV cache architecture analysis.
> *Semantic Companion Project Research Notes*. `/mnt/seagate/SemanticCrew/Research/
> Analysis/KVCache_RecallArchitecture_20260322.md`. QuietWire Research.

**Co-author question:** Chris Blask and Ashraf Al Hajj are co-developers and
should be consulted on authorship for papers touching CIOPS/CAP. Fred Cohen
contributed RAG architecture and catalog-for-retrieval methodology — citable
contribution and potential co-author. Diane's "recall vs. memory" observation:
if used as a founding distinction, she gets a citation or acknowledgment.

**AI disclosure (per ResearchNote_AIAuthorship_Attribution_20260323.md):**
The honest disclosure model for this project: Claude (Anthropic, claude-sonnet-4-6)
contributed to research synthesis, draft generation, literature search, and
analysis across sessions N+1 through N+19+. Framing, research questions,
epistemic ownership, and conclusions are the human researcher's. Specific AI
contributions should be noted by section in submitted manuscripts.

---

## Immediate Next Steps

1. [ ] Rewrite three PDF-formatted research notes as proper .md files
       (LLMSemanticDrift, ConfabulationCollision, ShannonToBoole) — N+19 action
2. [ ] Update Bloom field report with token-narrowing confound framing
3. [ ] Send Bloom field report to Anthropic (Bob action)
4. [ ] Design Bloom Run 3 with fixed scenarios and explicit fact-probing
5. [ ] Draft Paper 1 abstract (recall vs. memory) — enough material exists
6. [ ] Identify target journal for Paper 1 — AI/cognitive science intersection
       (candidates: Cognitive Systems Research, AI & Society, Minds and Machines)

---

## References

- Hillery, R. (2017). Short Course in Effective Communications (Paper_writing_101 v0.9).
  Teaching document, v0.9.
- Internal: BloomRun2_Results_20260316.md
- Internal: KVCache_RecallArchitecture_20260322.md
- Internal: ResearchNote_AIAuthorship_Attribution_20260323.md
- Internal: StoryOfAMind_Outline_N14.docx
- Internal: passdown_N18_to_N19_final.md

---
*Drafted N+19 | 2026-03-23 | Update each session as pipeline advances*
