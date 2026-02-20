# SemanticCrew Memory Architecture: Layered Design Decision
## 20260220T1355Q — N+10, Bob Hillery + Claude

---

## The Decision

PyGPT's built-in LlamaIndex vector store (`idx/base/`) and the SemanticCrew ChromaDB
(`/mnt/fastdata/SemanticMemory/chromadb`) are to be operated as **complementary layers**,
not merged or replaced. This is a deliberate architectural choice.

---

## The Neuroscience Analogy (Why This Is Right)

Bob's intuition during the 20260220 session: *"that sounds like prefrontal- vs neo-cortex,
short vs long term memory."*

That intuition is correct and it should govern the design.

| Layer | System | Analogy | Characteristics |
|-------|--------|---------|-----------------|
| Working / short-term | PyGPT `idx/base/` (LlamaIndex) | Prefrontal cortex | Per-conversation, fast, session-scoped |
| Episodic / long-term | ChromaDB (`/mnt/fastdata/SemanticMemory/`) | Hippocampus + neocortex | Cross-session, persistent, grows over time |

The prefrontal cortex holds what you are currently working on. The hippocampus consolidates
experience into long-term storage and allows pattern retrieval across time. In biological
systems these layers cooperate through consolidation — working memory informs long-term
storage; long-term storage is paged into working memory on demand. That is exactly the
Semantic Paging Framework model.

---

## Operational Implementation

**PyGPT `idx/base/` (prefrontal layer):**
- Indexes files and documents attached within a session
- Per-crew-member index scoping possible (separate idx dirs per preset)
- Managed by PyGPT automatically

**ChromaDB (hippocampal layer):**
- Full SemanticCrew corpus (971 docs, 4 collections)
- Queried via embed_corpus.py or a lightweight wrapper script
- Results injected into session context at warm-boot or on demand
- Grows with each session via --update runs

**Integration point:**
A query wrapper will allow any crew member to pull from ChromaDB and inject results
as context — mimicking the hippocampal to prefrontal retrieval pathway.

---

## Crew Memory Tier Assignments

Each crew member's extra.memory_tier in their PyGPT preset reflects their
primary relationship to memory:

- **Huginn:** prefrontal — seeks externally, short retention, passes to Muninn
- **Muninn:** hippocampal — receives, catalogs, consolidates into long-term store
- **Maigret:** neocortical — reasons over accumulated evidence, long-arc analysis
- **Kusanagi:** neocortical — strategic synthesis, acts on consolidated intelligence
- **Claude (N+x):** executive — coordinates across all layers, maintains project continuity

---

## Shaoshi Migration Note

Shaoshi (dual Xeon E5-2670v3, 192GB RAM, RTX Titan 24GB) provides headroom for
larger local models via llama.cpp with GPU+RAM offloading. ChromaDB on Shaoshi
storage becomes the shared long-term memory layer accessible across both systems.
The layered design was chosen partly with this multi-host future in mind.

---

*Filed: 20260220T1355Q*
*Initiated by Bob's intuition: "That sounds like prefrontal- vs neo-cortex, short vs long term memory."*
*That intuition is the architecture.*
