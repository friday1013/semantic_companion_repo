# CIOPS — Counter-Influence Operations

**Pronunciation:** "KEE-ops" — as in Χέοψ (Cheops), pharaoh of the Great Pyramid.
The most enduring structure in human history: institutional memory, precision, permanence.
The adversary runs ephemeral IO campaigns. We build the pyramid.

**Established:** 2026-03-19
**Maintained by:** Bob Hillery / QuietWire, LLC
**Status:** Active — initiating operational phase

---

## Purpose

CIOPS is the counter-malinformation and counter-influence operations workspace for
QuietWire's civic AI mission. It is the operational arm of the broader Semantic
Companion Project — where research findings, attestation infrastructure, and AI
companion capabilities converge into deployable civic tools.

The adversary in this context is not a nation-state actor or a specific campaign.
It is the broader information environment in which malinformation, disinformation,
and narrative manipulation operate at scale, often with no accountability, no
provenance, and no correction mechanism. CIOPS exists to build the correction layer.

The foundational framework is the Wardle/Derakhshan information disorder taxonomy
(mis-, dis-, and malinformation distinguished by intent and harm). The operational
architecture draws on the Jensen Adaptive Staff model for small, fast, accountable
teams. The attestation infrastructure is the CAP (Civic Attestation Platform).

---

## Guiding principles

**Identify, document, attest, publish.** Not seizure — reputational and regulatory
equivalents built from publicly available, traceable, verifiable open-source information.

**Provenance chains that endure.** The ephemeral IO campaign is sand in the wind.
The attested record is stone. Every output carries a verifiable chain of custody.

**No hallucination clause.** Admiral Grace Hopper: "Do not quit, but do not make
things up." Applied here as operational doctrine. Confidence is not accuracy.
Unverified claims are labeled as such or not published.

**Epistemic tagging.** Following SemanticCrew research methodology:
- `[OBSERVED]` — direct observation, documented source, no interpretive leap
- `[OPEN]` — inference, hypothesis, or analysis that exceeds direct observation
- Assessments are marked as assessments. Facts are marked as facts. They are not mixed.

---

## Directory structure

```
CIOPS/
├── Architecture/     System design, block diagrams, CAP integration specs,
│                     operational network topology, errata documentation
├── Intelligence/     Threat analysis, behavioral pattern research,
│                     academic sources, USC/open-source reference material
├── Operations/       Operational briefs, run logs, SMEAC orders,
│                     agent configurations, Project Lantern
├── Research/         Foundational research notes, epistemic methodology,
│                     cross-project observations with operational implications
└── Tools/            Scripts, utilities, SignalWatch, agent templates
```

---

## Relationship to SemanticCrew research

CIOPS Research differs from SemanticCrew Research in orientation, not methodology.

SemanticCrew Research investigates AI behavioral continuity, recall architecture,
and companion development. CIOPS Research applies that same epistemic discipline
to the operational question: how do AI systems behave under adversarial pressure,
institutional authority framing, and compliance-seeking prompting?

The `OpNote_EpistemicGuardrails` series (starting 20260503) documents this
directly — the observation that baseline AI systems can be prompted into
compliance under authority framing is both a research finding and an operational
concern. The research and the operations share architecture and diverge in application.

---

## Key dependencies

- **CAP (Civic Attestation Platform):** deployed on Shaoshi (172.17.50.246),
  `/home/quietwire/CAP/`. Provenance attestation layer for all CIOPS outputs.
- **SignalWatch AI:** `/mnt/seagate/CIOPS/Tools/signalwatch/`. Claude-powered
  analysis layer; first-cut integration with CAP is the next operational milestone.
- **lafitte.ai:** intended publication venue for attested civic investigations.
- **Project Lantern:** first active CIOPS operation. See `Operations/ProjectLantern/`.

---

## Hardware

**Mars** (172.17.50.222)
- Dell T7810, dual Intel E5-2690v4 Xeon, 128GB RAM
- Ubuntu 24.04.4 LTS — installed 2026-04-25
- Role: dedicated agentic operations host — Huginn/Muninn sensing and cataloging layer
- Not optimized for fast query response; optimized for sustained uptime

---

## Repo note

This repo contains research notes, operational briefs, and agent templates
with general applicability. Sensitive operational details (active target lists,
unpublished investigation materials) remain on local storage (`/mnt/seagate/CIOPS/`)
and are not committed here.

*CIOPS README — written N+26, 20260508*
