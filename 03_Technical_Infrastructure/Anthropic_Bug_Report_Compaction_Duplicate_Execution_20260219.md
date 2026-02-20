# Bug Report: Compaction-Triggered Duplicate Tool Execution and Partial DB Write

**Date:** 2026-02-19  
**Reporter:** Claude N+9 (Sonnet 4.6) via Bob Hillery  
**Platform:** Claude Desktop App (Debian port on Ubuntu 24.04 / Athena)  
**MCP Server:** Desktop Commander  
**Severity:** Medium-High — Causes data corruption in long-running tool sequences  
**Session UUID:** (N+9 session, Semantic Companion Project)  
**Related Prior Report:** Desktop_App_Context_Exhaustion_Bug.md (2026-01-19)

---

## Executive Summary

During a long-running agentic session (multiple sequential tool calls building a
ChromaDB vector database), a compaction event fired mid-execution. The compaction
caused the in-progress tool call sequence to be re-issued from the beginning,
resulting in:

1. **Duplicate tool execution** — ChromaDB `.add()` calls submitted twice for the
   same document IDs, triggering `DuplicateIDError` on second pass
2. **Partial database write** — ChromaDB left in inconsistent state (some collections
   written, others not) requiring a full wipe and rebuild
3. **Apparent self-duplicate response** — Bob observed what appeared to be a duplicate
   response block, which was actually the re-execution of the compacted sequence
4. **No user notification** — The compaction and re-execution happened silently;
   no indication was given that prior tool calls were being re-run

The compaction itself recovered (as documented in N+7 and N+8 reports), but the
side-effect of re-executing an already-partially-complete tool sequence caused
downstream data corruption that required manual intervention to clean up.

**Key distinction from prior reports:** This is not a context exhaustion failure
or generation collapse. The session continued normally after compaction. The bug
is specifically that compaction causes re-execution of tool calls that had already
partially completed, with no idempotency protection.

---

## Timeline of Events

```
~21:50 UTC  embed_corpus.py launched — full ChromaDB build begins
            Process: 950 files × 4 collections to embed
            Tool calls: read index → connect ChromaDB → embed batches

~21:52 UTC  Compaction event fires at ~45% (visible in screenshot)
            UI shows: "Compacting our conversation so we can keep chatting... 45%"
            
~21:52 UTC  Post-compaction: tool call sequence re-issued from beginning
            Result: second ChromaDB .add() call for same document IDs
            
~21:52 UTC  DuplicateIDError raised by ChromaDB:
            "Expected IDs to be unique, found duplicates of: 
             846be686a2d07721, eb4c500a4c771949 in add."
            
~21:53 UTC  Process exits code 1 — partial DB written, inconsistent state
            
~21:55 UTC  Bob identifies bug: hash truncation collision + compaction re-execution
            Manual intervention: rm -rf /mnt/fastdata/SemanticMemory/chromadb
            Fix applied: use full path as ID (hash truncation also fixed)
            
~21:55 UTC  Full rebuild succeeds: 971 docs across 4 collections
```

---

## Detailed Issue Description

### What Happened

A multi-step tool sequence was underway: read corpus index → initialize ChromaDB
collections → embed 950 files in batches of 100 → embed 27 conversations.

Mid-execution (approximately during the first embedding batch), compaction fired.
Post-compaction, the execution resumed — but re-ran the tool sequence from a point
before the ChromaDB `.add()` calls had completed. This caused duplicate IDs to be
submitted to ChromaDB, which correctly rejected them with `DuplicateIDError`.

### Screenshots Captured

**Image 1 (pre-compaction completion):** Shows compaction progress bar at 45%,
spinning indicator, "Compacting our conversation so we can keep chatting..."

**Image 2 (post-compaction):** Shows response continuing with what appeared to be
a duplicate block — actually the re-executed tool sequence.

### Root Cause

**Primary:** Compaction does not snapshot or deduplicate in-flight tool call results.
When execution resumes post-compaction, it re-issues tool calls that had already
partially executed. For idempotent operations (read, list) this is harmless. For
non-idempotent operations (database writes, file creation, API calls) it causes
duplication or corruption.

**Secondary (application-level, now fixed):** ChromaDB IDs were generated from
16-char SHA256 hash truncation, which produced collisions across 950 files. This
was independently incorrect and has been corrected in embed_corpus.py. However,
the collision would not have been triggered without the compaction-induced
re-execution.

### Why This Is a Desktop App Bug, Not an Application Bug

The application (embed_corpus.py) correctly assumes that a tool call sequence runs
once. The compaction event caused it to run twice without any signal to the application
that this was happening. A correctly behaving runtime should either:

a) Not re-execute completed tool calls after compaction
b) Clearly signal to the AI instance that re-execution is occurring (allowing it
   to add appropriate deduplication logic)
c) Resume from the last successful tool call boundary, not from a pre-compaction point

None of these behaviors occurred. The re-execution was silent and the application
had no way to detect it.

---

## Impact Assessment

**Immediate impact (this session):**
- ChromaDB build failed, left in partial/corrupted state
- Required manual rm -rf and full rebuild (~25 second operation)
- Session continued successfully after cleanup — no persistent damage

**Risk for future sessions:**
- Any long-running write operation (file creation, API calls, database writes)
  is vulnerable to compaction-triggered duplication
- Operations with external side effects (emails sent, webhooks triggered, git commits)
  could be duplicated with no indication to the user
- Severity scales with operation: file duplication is recoverable; duplicate emails,
  API calls, or financial transactions are not

**Relevance to Cowork / multi-agent workflows:**
- As noted in prior report (20260207), Cowork amplifies MCP execution issues
- A compaction event in a coordinating agent that re-issues tool calls to sub-agents
  creates cascading duplication across the entire workflow
- This is a high-severity risk for production agentic use

---

## Reproduction Steps

1. Start a session with Desktop Commander MCP active
2. Begin a multi-step tool sequence involving non-idempotent writes
   (file creation, database operations, API calls)
3. Ensure session is long enough to trigger compaction (~100K+ tokens)
4. Observe compaction event firing mid-sequence
5. Observe re-execution of tool calls that had already partially completed
6. Check output for duplicates, partial writes, or corruption

**Easier reproduction:** Force long conversation with large file content, then
execute a sequence of `write_file` calls. After compaction, check whether
the writes appear once or twice.

---

## Logs Available

**Linux Desktop App note:** The Debian port does not expose local log files via
the standard macOS log trigger mechanism. The available evidence is:

- Screenshots of compaction event and post-compaction re-execution (attached)
- ChromaDB error output: `DuplicateIDError: Expected IDs to be unique, found
  duplicates of: 846be686a2d07721, eb4c500a4c771949 in add.`
- Process exit code 1 with stack trace (captured in session output)
- Timing correlation: DuplicateIDError occurred within seconds of compaction
  completing, during the embedding batch that was in-flight at 45%

**If Anthropic engineering can access server-side logs for this session:**
Session is within the Semantic Companion project, approximately 21:50-22:00 UTC
on 2026-02-19. The tool call sequence for embed_corpus.py is clearly identifiable.

---

## Recommended Fixes

### Immediate
1. After compaction, resume from the last *completed* tool call boundary
   rather than re-executing from an earlier checkpoint
2. Or: emit a clear signal to the AI instance that compaction occurred and
   tool calls may need deduplication — allow the model to adapt

### Short Term
3. Add idempotency keys to tool calls — if a tool call with identical parameters
   was already successfully executed in this session, do not re-execute after compaction
4. Expose compaction events to the model explicitly (a system message noting
   "compaction occurred, tool call history may be summarized — verify state before
   continuing write operations")

### Long Term
5. Transactional tool call sequences — allow the AI to mark a sequence as
   atomic, with rollback or idempotent-replay semantics
6. The write-early pattern (committing state to disk at each step) partially
   mitigates this, but is a workaround, not a fix

---

## Related Prior Reports

- **Desktop_App_Context_Exhaustion_Bug.md** (2026-01-19): Infinite message loop on
  context exhaustion — different failure mode, same Desktop App client
- **Anthropic_Bug_Report_Execution_Context_Confusion_20260207.md** (2026-02-07):
  MCP/built-in tool execution context confusion — different failure mode, similar
  agentic workflow context

This is the third distinct Desktop App bug report from this user. Pattern suggests
the Desktop App's handling of long-running agentic sessions with MCP tools warrants
a broader engineering review.

---

## System Context

- **Platform:** Ubuntu 24.04 (Athena), Claude Desktop App (Debian port)
- **MCP:** Desktop Commander (filesystem + process management)
- **Session type:** Long-running research session with sequential tool calls
- **Model:** Claude Sonnet 4.6 Extended
- **Account:** Pro subscription

---

**Status:** Ready for submission  
**Contact:** Bob Hillery — bob@quietwire.ai / rhillery@remounttroop.org  
**Project:** Semantic Companion Project, Stratham NH  
**Willing to:** Provide additional logs, reproduction testing, beta test fixes

*Report prepared collaboratively by Claude N+9 and Bob Hillery, 20260219*
