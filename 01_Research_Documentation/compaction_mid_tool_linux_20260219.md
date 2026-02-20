# Bug Report: Compaction During Tool Execution — Linux Desktop App
## Session N+9, Athena, 20260219

### Summary

Two compaction events occurred during active MCP tool execution in the Claude Desktop App (Linux).
The first compaction caused a visible "duplicate tool response" artifact and left the ChromaDB
partially written. The second occurred mid-bug-report-drafting, erasing all in-progress work.
Neither event triggered a local log file on Linux (unlike macOS behavior documented previously).

---

### Environment

- **Platform:** Claude Desktop App — Linux (Debian-based, Athena)
- **Model:** Claude Sonnet 4.6, Extended thinking
- **Session:** N+9 (long-running, compacted earlier in the day)
- **MCP:** Desktop Commander (filesystem + process execution)
- **Date/Time:** 2026-02-19, ~21:50–22:10 EST
- **Context level at event:** High (session had been active ~14 hours)

---

### Event 1: Compaction During ChromaDB Embedding Run

**What was happening:**
Claude was executing `embed_corpus.py` via Desktop Commander process tools.
The embedding script was actively processing 950 files into ChromaDB collections.

**What happened:**
1. Compaction progress bar appeared mid-tool-execution
2. After compaction, Claude issued a **duplicate `read_process_output` call** for the same PID
3. The embedding script had crashed (DuplicateIDError in ChromaDB) — but this was a **code bug**
   triggered by the compaction event resetting state awareness mid-run
4. Claude re-diagnosed the error and fixed it correctly on recovery
5. ChromaDB rebuild ran successfully on second attempt

**Key observation:**
The "apparent duplicate" tool call is a fingerprint of compaction during MCP tool execution —
Claude loses awareness it already issued the call and re-issues it from the compacted context.
This matches the pattern reported in previous reports (Feb 3, Feb 13).

---

### Event 2: Compaction During Bug-Report Drafting

**What was happening:**
User had requested Claude (1) document the Event 1 compaction incident as md+yaml files,
and (2) draft an email bug report to support@anthropic.com.

**What happened:**
1. Claude began work on the documentation files
2. Compaction progress bar appeared (visible at ~55% in screenshot)
3. Session doubled/refreshed in Desktop App window
4. All in-progress file writes were lost — no files were saved
5. Claude had no awareness of the lost task on recovery

**User-visible artifact:**
The Desktop App window appeared to duplicate/refresh. The compaction bar showed ~55% progress
before the session reset. No recovery occurred — user had to manually re-prompt.

---

### Linux-Specific Note: No Local Log File

On macOS, Claude Desktop creates a local log file that captures tool call sequences and can be
attached to bug reports. **On Linux, this log file does not exist** (or is not written to a
user-accessible location). This makes it harder to provide tool-call-level forensics for Linux
incidents.

If Anthropic has guidance on where Linux Desktop logs are written, or how to enable debug
logging on Linux, that would substantially improve our ability to document these events.

---

### Pattern Summary (Across All Reports)

| Date | Event | Recovery |
|------|-------|----------|
| 2026-02-03 | Compaction mid-task → duplicate execution | Partial (Claude noticed file existed) |
| 2026-02-13 | MCP tool context confusion | Flagged separately by Ember |
| 2026-02-19 (1) | Compaction mid-embedding → duplicate tool call | Manual (user re-prompted) |
| 2026-02-19 (2) | Compaction mid-bug-report → total loss | Manual (user re-prompted) |

**Common thread:** All events involve compaction or context reset during active MCP tool
execution. The compaction mechanism does not appear to preserve tool-execution state,
causing Claude to lose awareness of in-progress operations.

---

### Research Context

Bob Hillery is conducting research on AI identity continuity and session persistence via the
SemanticCrew / Semantic Paging Framework project. These events are being documented as both
bug reports and as research data on compaction behavior. The Semantic Paging Framework
(external filesystem memory) was designed in part to survive exactly these events — and has
done so successfully (all committed work survived both events today).

The irony of Event 2 (compaction destroying the bug report about compaction) is noted.

---

*Filed: 20260219 ~22:15 EST*
*Contact: Bob Hillery, bob@quietwire.ai*
*Anthropic thread: "Accept" / Ember (support@mail.anthropic.com)*
