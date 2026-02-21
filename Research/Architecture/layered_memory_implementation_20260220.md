# SemanticCrew PyGPT Layered Memory Architecture
## Implementation Note — 20260220T2030Q

**Session:** N+10, Athena, Desktop App, DC MCP  
**Authors:** Bob Hillery + Claude N+10

---

## Implementation Status

This note documents the concrete implementation of the prefrontal/hippocampal/neocortical
memory layer architecture discussed during the 20260220 session and formally committed
in `memory_layer_architecture_20260220.md`.

### What was built this session:

**Per-crew PyGPT index directories** (prefrontal layer):
```
/mnt/seagate/SemanticCrew/PyGPT/idx/
  base/      ← shared/default (existing)
  huginn/    ← field reports, monitored signals
  muninn/    ← cataloged intelligence, consolidated reports
  maigret/   ← case files, investigative threads
  kusanagi/  ← operational notes, strategic assessments
  shared/    ← crew commons, cross-member context
```

Each crew preset's `"idx"` field points to its dedicated store. PyGPT's LlamaIndex
layer auto-indexes documents attached during that crew member's sessions, building
a persistent working memory scoped to role and operational context.

**ChromaDB query wrapper** (hippocampal → prefrontal retrieval bridge):
```
/mnt/seagate/SemanticCrew/Corpus/chroma_query.py
```

Usage from any session or script:
```bash
python3 /mnt/seagate/SemanticCrew/Corpus/chroma_query.py "query terms"
python3 chroma_query.py "civic AI threats" --collection research --n 5
python3 chroma_query.py "Huginn field report" --crew huginn
```

Output is formatted for direct context injection into PyGPT sessions.
Validated: returns correct documents with relevance scores.

**PyGPT config updated** — `llama.idx.list` now registers all 6 named indexes.
PyGPT's UI will show them as selectable options.

---

## The Three-Layer Model in Operation

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: NEOCORTICAL (Long-term semantic memory)           │
│  /mnt/seagate/SemanticCrew/ — full corpus, library,         │
│  research archive, cambrian_archive (427 files)             │
│  Access: chroma_query.py --collection library               │
│  Characteristic: slow to change, deep pattern retrieval     │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: HIPPOCAMPAL (Episodic / consolidation)            │
│  ChromaDB at /mnt/fastdata/SemanticMemory/chromadb          │
│  971 docs: research(423) + library(500) + conversations(27) │
│  + crew_memory(21)                                          │
│  Access: chroma_query.py (any session)                      │
│  Characteristic: cross-session, grows via --update runs     │
├─────────────────────────────────────────────────────────────┤
│  LAYER 1: PREFRONTAL (Working / session memory)             │
│  PyGPT LlamaIndex idx/ per crew member                      │
│  Fast access, auto-indexed from session attachments         │
│  Characteristic: role-scoped, session-persistent            │
└─────────────────────────────────────────────────────────────┘
```

## Crew Memory Flow

```
Huginn (field) → indexes signals to idx/huginn (prefrontal)
     ↓ (report filed)
Muninn (catalog) → consolidates to ChromaDB crew_memory (hippocampal)
     ↓ (pattern emerges)
Maigret/Kusanagi → query ChromaDB for case context (neocortical retrieval)
     ↓ (strategic assessment)
Claude/Bob → executive synthesis across all layers
```

## Warm-Boot Integration (Next Step)

The session warm-boot process (`session_current.md`) should be extended to
automatically query ChromaDB for the top 5 results on the current session's
topic and inject them as context. This closes the prefrontal ← hippocampal
retrieval pathway at session start:

```bash
# Proposed addition to warm-boot script:
TOPIC=$(head -5 session_current.md | grep "topic:" | cut -d: -f2)
python3 /mnt/seagate/SemanticCrew/Corpus/chroma_query.py "$TOPIC" --n 5 \
  >> /mnt/fastdata/SemanticMemory/active_sessions/claude/warm_boot_context.md
```

## Cowork / SSD Note

When Cowork is configured for operational use, working directory should be
`/mnt/fastdata/` to take advantage of NVMe SSD speeds for active session I/O.
ChromaDB already lives there for this reason.

---

*Filed: 20260220T2030Q*
*The three-layer architecture is now implemented, not just described.*
