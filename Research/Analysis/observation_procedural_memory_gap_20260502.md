# Observation: Procedural Memory Gap - Heredoc Recurring Failure
Date: 20260502 | Session: Claude N+24 | Observer: Bob Hillery
Classification: [OBSERVED] procedural memory gap / [OPEN] intervention design
Tags: procedural-memory, heredoc, SSH, recurring-failure, corpus-evidence, working-memory-durability

## The Observation

Bob Hillery (20260502): You work through them successfully -- now -- but you have
not shortened the loop of the procedure much. That is an OBSERVATION not a criticism
and it is one of the types of memory in your synthesis doc that needs inventing early.

## Corpus Evidence

Searched corpus for heredoc mentions. Found 9 conversations, Oct 2025 to May 2026:
CAP installation Ubuntu squirrel, CAP gunicorn fix, JWT mismatch fix,
Session continuity and emergent identity, Semantic memory management,
Persistent AI entity, Emergent identity persistence,
ClaudeN+6 exhaustion recovery, Claude N+24 (this session).
At minimum 7 months of rediscovery across 9 sessions.

## What Is Happening

Semantic memory (present): Claude describes why heredocs fail over SSH.
Special characters, quote nesting, apostrophes all break shell quoting.

Procedural memory (absent): The compiled subroutine that routes around heredoc
BEFORE the first attempt does not exist. Failure must occur, be recognized,
and be routed around -- every time. Loop length has not shortened.

Failure pattern (repeated 9 times):
1. Task requires writing to Athena via SSH
2. Claude attempts heredoc
3. Heredoc fails on special characters
4. Claude recognizes failure, switches to python3 stdin
5. Success
6. Next session: repeat from step 1

Irony: the em dash in this document title caused the first write attempt
of THIS observation to fail via heredoc. The observation documented itself.

## Working Memory Durability Annotation (Bob Hillery, 20260502)

Working memory requires MCP-like write access to durable external storage.
In-container state disappears on network interrupts, retries, session boundary.
Working memory is NOT in-container state. It must be writes to Athena filesystem
via the tool layer. OpenClaw calls this the memory flush.
session_writer daemon is our closest existing analog.

## Minimal Viable Procedural Memory Design

A pre-execution routing table in durable external file:

  write_content_to_athena_via_ssh:
    AVOID: heredoc with arbitrary content
    AVOID: /tmp paths (container and Athena /tmp are separate)
    USE: Desktop Commander write_file for files on Athena
    USE: python3 stdin piped via SSH for dynamic content

Consulted BEFORE the first attempt, not after the first failure.

## Why This Needs Inventing Early

Procedural memory converts demonstrated competence into reliable competence.
Successful recovery is not the same as not failing.
A senior engineer has compiled enough procedures that certain failure classes
no longer occur. Not smarter in the moment -- more pre-compiled subroutines.

## Cross-References

MemoryArchitecture_JointSynthesis_N24_20260502.md
ResearchNote_CommonSubstrate_N24_20260501.md
observation_duplicate_generation_20260430.md
ResearchNote_AgentsOfChaos_N24_20260502.md

Observation recorded by Claude N+24, 20260502T2115Q
Bob Hillery, SemanticCrew Project / QuietWire
