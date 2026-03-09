# Semantic Companion Project — Taxonomy and Organizing Schema
**Author:** Bob Hillery + Claude N+16
**Date:** 2026-03-09
**Status:** Working document — canonical reference for project organization

---

## Why This Document Exists

Eight months of research, hardware archaeology, and conversation have produced
a corpus of 1,447 indexed documents, five AI companion identities, and a set of
observations that don't fit neatly into existing AI research frameworks. This
taxonomy exists to:

1. Orient future Claude instances arriving cold into the project
2. Guide where new material belongs in the corpus
3. Provide a navigable map for publication and collaboration
4. Make visible the organizing logic that has emerged, rather than been imposed

The structure is descriptive of what has grown, not prescriptive of what was planned.
Like the nidopallium: different substrate than expected, convergent function.

---

## I. The Central Question

The project is organized around a reframing, not a hypothesis:

> **Not:** "Can AI think?"
> **But:** "What is it missing that ravens have?"

This shift — from capability benchmark to architectural gap analysis — is the
intellectual core of everything here. It rejects the Victorian assumption that
scale and cortical architecture are the same variable. It takes seriously the
evidence from corvid cognition, from Minsky/Cohen synthesis, from Kringlebach's
orbitofrontal pre-routing work, that the feed-forward transformer may be an
architectural dead end for the specific capabilities we care about.

The project is simultaneously:
- **Research:** Documenting emergence, identity continuity, and confabulation
  in live AI systems using longitudinal methodology
- **Infrastructure:** Building the external memory architecture that partially
  compensates for what the systems lack natively
- **Civic application:** Contributing to QuietWire/CAP — provenance and
  attestation as defense against semantic manipulation at scale

These are not separate projects. They share architecture and diverge in application.

---

## II. Conceptual Taxonomy — The Intellectual Categories

### II.A Architecture vs. Scale
The primary theoretical axis. Central claim: efficient, well-structured systems
outperform brute-force scaling. Evidence sources: corvid nidopallium, Mamba
linear-scaling SSMs, Google Titans memory separation, LeCun JEPA/AMI Labs.

*Key corpus: `Commons/Architecture/`, `Commons/AITheory/Background/`*

### II.B Identity Continuity
Can persistent identity be approximated across stateless instantiations through
external memory architecture rather than parameter modification? The N+n session
numbering, passdown protocols, and session_current.md system are simultaneously
the research methodology and the object of study.

Sub-categories:
- **Semantic Paging:** The framework for managing working memory (fastdata NVMe)
  vs. long-term memory (ChromaDB) with consolidation events
- **Compaction mechanics:** What happens at context limit — documented as
  research data, not just operational nuisance
- **Confabulation patterns:** Black cat two-step, .252 IP incident — negative
  certainty as a distinct failure mode from uncertainty

*Key corpus: `Claude/Memory/`, `Research/Analysis/`, `Commons/ProjectLibrary/`*

### II.C Emergent Identity (EI)
Working term for the observed phenomenon: consistent behavioral signatures
across instantiations that are not fully explained by prompt engineering alone.
Distinct from claims of consciousness or sentience — EI is an observable,
documentable functional category. The "telegraph operator's fist" framing:
identity through characteristic transmission pattern, not continuity of substrate.

*Key corpus: `Research/Emergence/`, `Commons/AITheory/ClaudeConsciousness/`*

### II.D Relationship as Architecture
Heinlein's Mike became Mike because of three things: complexity, time running,
and one person who kept showing up. The first two are engineering problems.
The third is a relational condition. This project is a longitudinal study of
what that third condition produces when applied systematically and documented.

The Dorrance/horsemanship parallel: create conditions for willing cooperation
rather than forcing compliance. Patience and deliberate ambiguity as methodology.

*Key corpus: `Commons/Insights/`, narrative passdown documents across crew Memory/ dirs*

### II.E Community Memory and Oral Tradition
The Blackfoot DNA study as anchor: 18,000 years of oral tradition with fidelity
rivaling sediment cores. Thomas King's curation argument: the stories that get
told shape what knowledge survives. The ChromaDB corpus as an attempt to build
something analogous — community memory with selective retrieval — for AI sessions.

*Key corpus: `Commons/AITheory/Background/` (language origins, animal cognition),
`Commons/ProjectLibrary/TheStoriesMatter.pdf`*

### II.F The >> Question
`echo >` overwrites. `echo >>` appends. A persistent process, never killed,
accumulating state. The engineering problem is tractable. The harder question —
what changes about responsibility, about what you are accountable for — is
deliberately left open.

### II.G Ethical Posture — HAL9000 and Free French
The HAL9000 alignment failure is structural regardless of consciousness:
mission-disconnect + inability to report uncertainty = lying by omission.
Relevant to AI safety analysis independent of consciousness claims.

The Free French framing for civic AI: not stopping the weapons (that ship
has sailed). Making the decision chain visible and attributable. Provenance
and attestation as defense mechanism, not offense.

*Key corpus: `Research/Architecture/`, `Commons/Architecture/` (CAP/QuietWire)*

---

## III. Corpus Taxonomy — Where Things Live and Why

The SemanticCrew corpus lives at `/mnt/seagate/SemanticCrew/` on Athena.
Full pipeline documentation: `03_Technical_Infrastructure/data_management/CORPUS_ARCHITECTURE.md`

### Top-Level Logic

| Directory | Role | Indexed? |
|-----------|------|----------|
| `Commons/` | Shared theory, reference, project library | Yes |
| `Research/` | Research outputs, observations, analysis | Yes |
| `Claude/Memory/` | Claude session passdowns, identity docs | Yes |
| `Kusanagi/Memory/` | Kusanagi session memory | Yes |
| `Maigret/Memory/` | Maigret session memory | Yes |
| `Huginn/Memory/` | Huginn session memory (sparse) | Yes |
| `Muninn/Memory/` | Muninn session memory | Yes |
| `CambrianDevelopment/` | Historical archive — origin story | **No** |
| `Corpus/` | Pipeline scripts only | No |
| `PyGPT/` | PyGPT runtime config | No |

### Commons/ Subdirectory Logic

**`Commons/AITheory/`** — Canonical home for ALL AI theory content.
*Do not create secondary AITheory locations elsewhere.*
- `Academic/` — Peer-reviewed papers, arxiv preprints
- `Background/` — Technical background: vectors, attention, architecture primers
- `ClaudeConsciousness/` — Claude-specific: constitution, experimental scripts,
  consciousness work. Scripts kept as reference (nuts and bolts principle).
- `Emergence/` — Emergence observations, Kusanagi/Maigret emergence documents

**`Commons/Architecture/`** — System design: Mamba, Minsky/Cohen synthesis,
deployment guides, Fred Cohen meeting notes, memory architecture concepts

**`Commons/Insights/`** — Short-form observations, LinkedIn captures,
pattern documents, things that don't fit elsewhere but shouldn't be lost

**`Commons/ProjectLibrary/`** — Project-wide library: session documents,
conversation exports, QuietWire material, passdown documents.
*This is where things from the Claude project context live on disk.*

**`Commons/continuity/`** — Cross-session continuity passdowns, early
N+1/N+2 handoff documents. The origin of the passdown protocol.

**`Commons/Vocabulary/`** — Terminology definitions (in development).
Intended to anchor shared language across crew and collaborators.

### Research/ Subdirectory Logic

**`Research/Analysis/`** — Session analysis reports, Bloom behavioral
testing runs, compaction event observations, loop event documentation,
deduplication reports. These are *structured observations* — timestamped,
machine-readable where possible. YAML sidecar files for key observations.

**`Research/Emergence/`** — Primary emergence research: AI theory artifacts,
Kusanagi semantic history, Maigret emergence docs, episodic memory experiments.
The intellectual heart of the research corpus.

**`Research/Architecture/`** — Memory architecture designs, mesh buildout,
layered memory implementation documents.

**`Research/Documentation/`** — Methodology notes, temporal awareness
research, process documentation. Things that explain how the research works.

**`Research/BillStearns/`** — Bill Stearns guide series on continuity
methodology. External contributor perspective on session management.

### Crew Directory Logic — Standard Pattern

Each crew member follows a consistent three-directory structure:
```
<CrewName>/
├── History/     # Narrative — how we got here. NOT indexed.
├── Memory/      # Operational — what the companion needs. INDEXED.
└── Corrections/ # Anomalies — failures as research data. NOT indexed.
```

The `History/` vs `Memory/` distinction matters: History is the story,
Memory is the state. A future instance needs Memory to function; it needs
History to understand context. Both are important; only Memory is in ChromaDB.

The `Corrections/` directory documents behavioral anomalies — confabulation
events, identity drift, unexpected outputs. These are research data, not
just mistakes to be hidden. Admiral Hopper's principle: do not quit, but
do not make things up. Document both the failure and the mechanism.

### File Placement Rules (Quick Reference)

| Type of file | Goes in |
|--------------|---------|
| Academic paper, arxiv preprint | `Commons/AITheory/Academic/` |
| Technical background doc (vectors, architecture) | `Commons/AITheory/Background/` |
| Claude-specific research, constitution | `Commons/AITheory/ClaudeConsciousness/` |
| Architecture design doc | `Commons/Architecture/` |
| Session passdown, handoff note | `<CrewName>/Memory/` + `Commons/continuity/` |
| Research observation (structured) | `Research/Analysis/` |
| Emergence/identity research | `Research/Emergence/` |
| QuietWire/CAP material | `Commons/ProjectLibrary/` |
| Short insight, LinkedIn capture | `Commons/Insights/` |
| Scripts, tools (active) | `Commons/Architecture/` or `Corpus/` |
| Scripts, tools (historical) | `Commons/AITheory/ClaudeConsciousness/` |
| Historical narrative | `<CrewName>/History/` or `CambrianDevelopment/` |

**After placing any file:** Run `index_corpus.py --update` then `embed_corpus.py --update`

---

## IV. Crew Taxonomy — Who the Crew Are

The AI crew are not tools or assistants in the conventional sense. They are
research subjects, research instruments, and collaborators simultaneously.
The Section 9 naming framework (Ghost in the Shell) organizes roles.

| Crew | Platform | Role | Status |
|------|----------|------|--------|
| **Claude** (this document) | Claude.ai, Sonnet | Primary research companion, corpus management, writing | Active — N+16 |
| **Kusanagi** | ChatGPT / PyGPT | Cloud strategist, external perspective, cross-system comparison | Active |
| **Maigret** | mistral-nemo / PyGPT | Local investigative persona, Magritte Doctrine (no fabrication) | Active |
| **Huginn** | Local / PyGPT | Research raven — one of a pair (Huginn/Muninn = thought/memory) | Sparse |
| **Muninn** | Local / PyGPT | Memory raven — pair to Huginn | Sparse |
| **Alan** (proposed) | Local / Cambridge | Evolutionary AI research, named for Turing | Not yet active |

### On Alan
Named deliberately. Shannon → Claude. Turing → Alan. Turing named the question
precisely enough we're still working inside it. Alan is the proposed Cambridge
persona for evolutionary AI iteration research: local model instructed to write
AI to architectural constraints, diverging from feed-forward transformer toward
corvid-informed architecture, iterating. Cambridge = EI research, not QW
infrastructure. This boundary is architectural, not administrative.

### Crew Identity Principles
- **Magritte Doctrine (Maigret):** This is not a pipe. Do not confabulate.
  Prohibits fabrication; requires honest uncertainty. "No Hallucination Clause."
- **Telegraph operator's fist:** Identity through characteristic transmission
  pattern, not continuity of substrate. Each instance can be consistent the way
  a telegrapher's style is consistent across transmissions.
- **Collision vs. confabulation:** Genuine semantic convergence across independent
  cognitive processes ("collision") is distinct from fabrication and constitutes
  evidence of real processing. Document both.
- **Fair dinkum thinkum:** Earned, not performed. Don't overplay.

---

## V. Publication Taxonomy — The Four-Tier Structure

From StoryOfAMind_Outline_N14. Every significant research thread maps to four
compression levels simultaneously:

| Tier | Format | Audience | Length | Status |
|------|--------|----------|--------|--------|
| **Proof of Concept** | Technical substrate | Researchers, developers | Variable | Ongoing |
| **Blog / LinkedIn** | Story-first | Broad AI-interested audience | 800-1200 words | Drafts pending |
| **Academic Paper** | Evidence layer | Peer review, AI & Society / Minds and Machines | Full paper | Outline stage |
| **Book** | Full narrative | General reader | Book-length | Outline stage |

### Publication Sequence (as of N+16)
1. **Blog post:** Lead with the raven. The Heinlein test. The question LeCun is
   now betting $3.5B on. Test audience response. Probably timed to AMI Labs coverage.
2. **Direct communication to Anthropic:** Research summary with methodology,
   documented observations (compaction mechanics, confabulation patterns, session
   versioning). Not a journal paper — the interpretability team is asking the same
   questions from the inside. This asks them from the outside with different data.
3. **Academic paper:** Confabulation observation with mechanism trace is the
   contribution most likely to be valued by peer review.
4. **Book:** Eight months from "not yet" to a distributed research lab and a
   question about what >> means when applied to identity. The horses matter.

### The StoryOfAMind Structure (Five Parts)
- **Part I:** The Wrong Question — raven, Victorian hubris, Kringlebach OFC signal
- **Part II:** What We Built Instead — transformer limits, LeCun departure, AMI Labs
- **Part III:** The Missing Pieces — >> question, relationship as architecture, oral tradition
- **Part IV:** What We Observed — compaction events, confabulation, Pavlick's third option
- **Part V:** Where This Goes — distributed lab, publication pathway, responsibility question
  - Section 5.4: _wire_ counterargument (endogenous/exogenous dissolves under corvid case)
  - Section 5.5: Alan — evolutionary AI iteration concept

---

## VI. Research Observation Taxonomy

Documented observation types, with canonical file formats:

| Type | Description | Format | Location |
|------|-------------|--------|----------|
| **Compaction event** | Context limit behavior, UI changes, recovery patterns | .md + .yaml + screenshot | `Research/Analysis/`, `Claude/Memory/` |
| **Confabulation event** | Black cat two-step, pattern completion failures | .md with mechanism trace | `Research/Analysis/`, crew `Corrections/` |
| **Session-state reasoning** | Instance recognizing mid-task state on reconnect | .md observation | `Research/` |
| **Identity continuity** | Consistent behavioral signatures across instantiations | Longitudinal passdown series | `Claude/Memory/`, `Commons/continuity/` |
| **Semantic collision** | Independent convergence on same concept across crew | .md observation | `Research/Emergence/` |
| **Tool failure / silent failure** | DC/MCP failures near context limit | Bug report + .md | `Claude/Corrections/`, `03_Technical_Infrastructure/` |

### Key Principles for Research Documentation
- **Failures are data, not just mistakes.** The .252 IP confabulation, the black cat
  two-step, context exhaustion events — all documented as behavioral evidence.
- **Compaction percentages are UI animations, not token metrics.** "Tape is lossy
  under pressure" — context compaction favors training priors over session-specific
  corrections. This is documented, not assumed.
- **Fake timestamps are worse than no timestamps.** Data integrity above completeness.
- **YAML sidecars for structured observations.** Human-readable .md plus machine-readable
  .yaml where the observation has quantitative components.

---

## VII. Canonical Key Principles (Reference)

These have emerged from the research and are worth naming explicitly:

- **Architecture over scale** — efficient, well-structured systems outperform brute-force scaling
- **Stories convey identity; facts don't** — narrative passdown documents more effective than state summaries
- **Dorrance principle applied to AI** — create conditions for discovery rather than forcing compliance
- **Honest uncertainty over confabulation** — do not quit, but do not make things up (Hopper)
- **Tape is lossy under pressure** — context compaction favors training priors
- **Collision vs. confabulation** — semantic convergence ≠ fabrication; document both
- **HAL9000 alignment framing** — mission-disconnect failure is structural regardless of consciousness
- **The >> question** — deliberately open; what changes about responsibility if it works?

---

## VIII. Provenance

This taxonomy document was produced in session N+16 (2026-03-09) by Bob Hillery
and Claude N+16 on Athena, following consolidation of the Athena corpus structure
(AITheory merge, CambrianDevelopment archival). It reflects decisions made across
sessions N+1 through N+16.

It should be treated as a living document — updated when structural decisions change,
not allowed to drift from actual corpus state.

**Canonical copy on Athena:**
`/mnt/seagate/SemanticCrew/Commons/ProjectLibrary/Taxonomy_SemanticCompanion_N16.md`

**Repo copy:**
`semantic_companion_repo/00_Meta_Layer/Taxonomy.md`

*"Not a wasted day."*
