# SemanticCrew Folder Structure
**Last updated:** 2026-03-09 N+16

This document describes the canonical directory layout of the SemanticCrew corpus
on Athena (`/mnt/seagate/SemanticCrew/`). See `CORPUS_ARCHITECTURE.md` for the
indexing pipeline and ChromaDB collection details.

---

## Top-Level Layout

```
/mnt/seagate/SemanticCrew/
├── Claude/              # Claude-specific history, memory, corrections
├── Kusanagi/            # Kusanagi (ChatGPT) crew files
├── Maigret/             # Maigret (mistral-nemo/PyGPT) crew files
├── Huginn/              # Huginn crew files (transitioning to PyGPT)
├── Muninn/              # Muninn crew files
├── Commons/             # Shared, cross-crew resources (INDEXED)
├── Research/            # Research outputs, analysis, emergence docs (INDEXED)
├── Corpus/              # Pipeline scripts only (index_corpus.py, embed_corpus.py)
├── CambrianDevelopment/ # Historical archive — NOT indexed (see note below)
└── PyGPT/               # PyGPT runtime config and session data
```

---

## Commons/ — Shared Resources (Indexed)

```
Commons/
├── AITheory/            # Canonical location for ALL AI theory content
│   ├── Academic/        # arxiv papers, peer-reviewed research
│   ├── Background/      # Technical background: vectors, attention, architecture
│   ├── ClaudeConsciousness/  # Claude-specific: constitution, consciousness work,
│   │                         # early experimental scripts (kept as reference)
│   └── Emergence/       # Emergence observations, Kusanagi/Maigret emergence docs
├── Architecture/        # System architecture docs, Mamba/Minsky/Cohen, deployment
├── Insights/            # LinkedIn posts, short-form observations, pattern captures
├── ProjectLibrary/      # Project-wide library: session docs, exports, QW material
├── continuity/          # Cross-session continuity passdowns
└── Vocabulary/          # Terminology and concept definitions (in development)
```

**Note on AITheory:** In N+16 (2026-03-09), all unique content from
`CambrianDevelopment/Infrastructure/AITheory/` was merged here via
`rsync --ignore-existing`. CambrianDevelopment is no longer indexed.
46 new documents were added.

---

## Crew Directories — Standard Layout

Each crew member (Claude, Kusanagi, Maigret, Huginn, Muninn) follows this pattern:

```
<CrewName>/
├── History/     # Narrative docs, session transcripts, conversation exports
│                # Content: the "how we got here" story for this companion
├── Memory/      # INDEXED: passdowns, session state, identity docs
│                # Content: what the companion needs to function
└── Corrections/ # Documented error events, confabulations, behavioral anomalies
                 # Content: research data — failures are data, not just mistakes
```

**Important distinction:** `Memory/` is indexed and embedded (ChromaDB `crew_memory`
collection). `History/` is NOT indexed — it's narrative/archival, not operational.

---

## Research/ — Research Outputs (Indexed)

```
Research/
├── Analysis/       # Session analysis, Bloom runs, compaction observations,
│                   # deduplication reports, loop events
├── Architecture/   # Memory architecture designs, mesh buildout docs
├── Documentation/  # Temporal awareness, methodology notes
├── Emergence/      # Core emergence research, AI theory artifacts
│   ├── JANA/
│   ├── Kusanagi-SemanticHistory/
│   ├── Maigret/
│   ├── Mind/
│   ├── chat_archives/
│   ├── episodic_memory/
│   ├── logs/
│   ├── memory_seeds/
│   └── system/
└── BillStearns/    # Bill Stearns guide series (continuity methodology)
```

---

## CambrianDevelopment/ — Historical Archive (NOT Indexed)

This directory is the origin story — QW-era work, Kusanagi creation logs,
early infrastructure experiments, and the Semantic Disruption/Civic AI framing
that preceded the current research arc.

**Why it's retained:** Like a box of old hardware — you don't know when you'll
need the reference. "That was 3rd grade arithmetic... wait, I need dot products now."

**Why it's not indexed:** All unique technical content has been merged into
`Commons/AITheory/`. Double-indexing creates noise in ChromaDB queries.
The narrative and image content (`.pages`, `.png`, `.jpg`) is not queryable
in ways that benefit the research pipeline.

---

## Corpus Pipeline Scripts

```
Corpus/
├── index_corpus.py      # Stage 1: scan LIBRARY_DIRS, build corpus_index.json
├── embed_corpus.py      # Stage 2: read index, embed into ChromaDB
├── chroma_query.py      # Direct ChromaDB query utility
├── CORPUS_ARCHITECTURE.md  # Canonical reference — read before touching scripts
└── UPDATE_STRATEGY.md   # When to run full rebuild vs --update
```

**Always run index before embed.** See `CORPUS_ARCHITECTURE.md` for full pipeline docs.
