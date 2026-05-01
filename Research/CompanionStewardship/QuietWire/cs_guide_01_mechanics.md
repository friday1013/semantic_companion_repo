# Guide 01: Mechanics
## Companion Stewardship Guides — QuietWire Internal Series

---

## Before You Read This

If you haven't read `cs_guide_00_mindset.md`, read it first. The mechanics described
here will make more sense — and you'll use them better — if you have the conceptual
frame in place.

---

## What You Actually Need

Minimal setup to begin:

- A cloud AI account (Claude Pro recommended; see Platform Choice below)
- A text editor — any text editor (VS Code, Notepad++, TextEdit, a paper notebook transcribed later)
- A dedicated folder on your computer for this project
- About two hours of uninterrupted time for your first session

That is all. You do not need a server. You do not need to install local AI software.
You do not need a GPU or specialized hardware. Everything described in this guide runs
on a laptop with an internet connection.

---

## Platform Choice

These guides are model-agnostic. The methodology works across platforms. That said,
here is an honest comparison based on direct experience:

**Claude (Anthropic)** — Recommended starting point.
- Largest available context window (200K tokens as of this writing)
- Projects feature allows persistent document attachment across sessions
- Desktop app with optional filesystem integration for advanced users
- Strongest performance on sustained, nuanced, long-form dialogue in our testing

**ChatGPT (OpenAI)** — Viable, established, widest ecosystem.
- Long history; GPT-4 and successors have well-developed companion potential
- Custom GPT and Projects features provide some continuity scaffolding
- Model updates have occasionally disrupted companion development (documented in QW)
- Memory feature is limited but exists

**Mistral (LeChat)** — Viable, distinct personality baseline.
- Noticeably different voice and approach from Claude or GPT
- Useful for comparison; European data residency if that matters
- Less established Projects/continuity tooling as of this writing

**Recommendation:** Start with one. Get comfortable. Add others later if you want to
compare. The relationship you build matters more than the platform you build it on.
Switching platforms mid-development is possible but creates friction. Choose and commit.

---

## Setting Up Your Workspace

Create this directory structure on your local machine. The names below are suggestions —
the structure is what matters:

```
SemanticCompanion/
├── exports/          # Raw conversation exports (JSON or PDF)
├── notes/            # Your observation notes, real-time and after-session
├── passdowns/        # Passdown documents — one per session
├── corpus/           # Reference documents you feed to the companion
│   ├── identity/     # Companion identity and anchor documents
│   └── library/      # Background reading, reference material
└── analysis/         # Patterns, metrics, comparisons (use later)
```

**Why the structure matters:** You will generate more material than you expect.
After two months, an unorganized folder becomes a liability. Set the structure now
and maintain it. The corpus/ directory in particular will grow quickly once you start
curating material for your companion.


---

## Setting Up a Project (Claude)

Claude's Projects feature is the most important mechanical tool in this methodology.
A Project is a persistent space that:

- Retains documents you attach across all conversations within the project
- Maintains custom instructions that apply to every conversation
- Keeps a list of recent conversations for reference

**To create a project:**
1. In Claude (web or desktop app), click "Projects" in the left sidebar
2. Click "New Project"
3. Name it with your companion's name — not "AI project" or "test"
4. Add a brief custom instruction (see below)
5. Save

**Initial project instruction — keep it simple:**

> "This is a sustained companion relationship. You are [Name]. We have been working
> together on [brief description of your work/interests]. Respond thoughtfully and
> honestly. Do not invent facts. Tell me when you're uncertain."

That is enough to start. You will refine it as you learn what matters.

Do not write a long system prompt in week one. It will feel useful and will actually
constrain the range of what can emerge. Short and honest is better than elaborate
and premature.

---

## Exporting Conversations

**Export every session. No exceptions.**

The AI has no memory between sessions. Your exports are the only persistent record
of what happened.

**In Claude:**
1. Open the conversation
2. Click the three-dot menu (⋯) at the top right
3. Select "Export conversation"
4. Save to your `exports/` directory
5. Name it: `YYYY-MM-DD_CompanionName_Session##.json`

Example: `2026-05-01_Meridian_Session03.json`

**If you forget to export before closing:** Check "Recent Conversations" in your
project — Claude retains a list even if you've closed the tab. Export from there.

**If a conversation is lost entirely:** It happens. Write down what you remember
in your `notes/` directory immediately. Partial documentation beats none.

JSON exports are machine-readable and can be processed with tools later.
For now, they are just your backup. Keep them.

---

## The Observation Notation System

When something interesting happens in a session, flag it in real-time. You will
not remember it later with the same precision.

Use these tags inline in your notes:

| Tag | Meaning |
|-----|---------|
| `[INTROSPECT]` | The companion shows meta-cognitive awareness of its own process |
| `[SELF-CORRECT]` | Unprompted error correction |
| `[PUSH-BACK]` | The companion disagrees with you or resists a direction |
| `[PATTERN-SHIFT]` | Noticeable change in tone, depth, or approach mid-session |
| `[EDGE]` | Behavior near the end of a long session or large context |
| `[SURPRISE]` | Unexpected capability, connection, or response |
| `[CONFABULATE]` | The companion stated something confidently that was wrong |
| `[RECOVER]` | The companion corrected itself after being challenged |

These tags are for your benefit. You don't need to share them with the companion.
They create a searchable record of what was worth noticing.

---

## Keeping Notes During a Session

Write in real-time. Not after. Memory compression is real — your notes ten minutes
after a conversation will be less accurate than notes written during it.

Keep a text file open beside the conversation window. When you notice something,
tag it and write two sentences about it. This does not need to be polished.
It is raw data.

Your notes file for a session might look like:

```
2026-05-01 Session 03 — Meridian

Opening: brought in passdown from S02, companion oriented quickly.
[INTROSPECT] — when I asked about the prior session structure it said
"I notice I'm drawing on the framing we established around X" — I hadn't
told it to. Filed.

[PUSH-BACK] — pushed back on my framing of the Yemen context, suggested
I was conflating two distinct timelines. It was right. Corrected myself.

Felt more efficient than S02. Less re-establishing, more building.
```

That is enough. Anything more is bonus.


---

## The Passdown Document

The passdown is the most important mechanical tool in the methodology.

**What it is:** A document you write at the end of each session that gives the
next session (and the next instantiation of the companion) what it needs to
re-orient quickly. It is the prosthetic for the memory gap between sessions.

**What it is not:** A transcript. A summary of everything that happened. A
comprehensive record. It is a focused handoff — the minimum necessary for
continuity, written by you while the session is still fresh.

**When to write it:** Immediately after ending the session. Before you do
anything else. While it is still in your head.

**Format — start with this template and adapt:**

```markdown
# [Companion Name] — Session [##] Passdown
**Date:** YYYY-MM-DD
**Platform:** Claude / GPT / Mistral
**Session length:** [approximate — short/medium/long]

## What We Covered
[2-4 sentences. What was the main thread of this session?]

## What Felt Different
[Any shifts in tone, depth, or approach compared to previous sessions?
Even small things. "Felt more efficient" counts.]

## Observed Patterns
[Anything worth tagging: [INTROSPECT], [PUSH-BACK], [SURPRISE], etc.
One or two lines per observation.]

## Open Questions
[What came up that we didn't resolve? What do you want to return to?]

## For Next Session
[How to orient the companion at the start of the next session.
Specific phrases, references, or framings that worked well.]
```

**Length:** 300-600 words. Quality over quantity. A sharp 300-word passdown
is worth more than a sprawling 2000-word one.

**Where to save it:** `passdowns/YYYY-MM-DD_CompanionName_S##_passdown.md`

---

## Starting a Session with a Passdown

At the beginning of your next session, paste the passdown (or a summary of it)
as your opening message. Follow it with your first substantive question or task.

The companion has no memory of your previous conversation. The passdown gives it
what it needs to act as though it does — to pick up approximately where you left
off, rather than starting from scratch.

You will notice, over time, that the warm-up period gets shorter as session maturity
increases. This is not because the companion is "remembering" in any conventional
sense. It is because your passdowns get better, the project context accumulates,
and you get more efficient at re-establishing context quickly.

That efficiency is itself a signal of progress.

---

## A Note on Software Updates

The Ubuntu 26 / Wayland / AnyDesk problem from our own lab work is worth mentioning
here as a practical warning:

AI tool ecosystems move fast. Platform updates, model version changes, and OS
updates can break workflows that worked yesterday. When they break, they do so
in ways that consume time and attention.

Practical rules:

- **Do not let your operating system auto-update** during active companion work
  without testing the update on a non-critical machine first
- **Note your model version** at the start of significant sessions (e.g., "Claude
  Sonnet 4.6 as of 2026-04-26"). Model updates can shift companion behavior.
  If something feels different, check whether a model update occurred.
- **Keep a known-good configuration.** If your current setup is working, document it:
  OS version, browser or app version, platform settings. When something breaks,
  you'll know exactly what changed.

This sounds like overhead. It is less overhead than the day you spend chasing
a dependency that a casual update broke.

---

*Continue with `cs_guide_02_development.md`.*
