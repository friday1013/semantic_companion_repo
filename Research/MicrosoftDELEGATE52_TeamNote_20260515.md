# Shared Reading: Microsoft Research on AI Agents and Document Workflows
**For:** #tools-testing-capabilities (and broader QW team)
**Date:** 20260515
**Source:** "LLMs Corrupt Your Documents When You Delegate" — Microsoft Research
(Philippe Laban, Tobias Schnabel, Jennifer Neville)
**Coverage:** https://techstrong.ai/articles/microsoft-study-warns-ai-agents-corrupt-data-in-long-workflows/

---

This is worth reading by everyone building with or evaluating AI agents right now.
Sharing because it's directly relevant to where we are as a team and as a product.

---

## What they studied

Microsoft Research built a benchmark called DELEGATE-52 — 52 professional domains
(accounting, crystallography, legal drafting, etc.) — and tested what happens when
you delegate multi-step document workflows to frontier AI models. Models tested
included GPT-5.4, Gemini 3.1 Pro, and Claude 4.6 Opus. This isn't a critique of
any one vendor; it covers the whole current generation.

## What they found

**The headline number:** Frontier models lost an average of 25% of document content
over 20 interactions. Averaged across all models tested, degradation reached 50%.

**The failure pattern is not gradual drift.** Errors happened in bursts — a single
interaction could wipe out 10-30% of a document's integrity in one step. By the
time you notice, the damage is already done.

**Better models fail differently, not less.** Weaker models tend to delete content.
More capable frontier models tend to corrupt it — meaning the document still looks
complete and coherent, but the content has changed. Subtle corruption is harder to
catch than obvious deletion.

**Agentic tooling made things worse, not better.** Giving models access to file
systems and code execution (the standard "agentic harness") added an additional
6% degradation on average. More autonomy, more risk.

**The readiness bar they set:** 98% accuracy. One domain met it: Python coding.
In 80% of all other simulated conditions, models severely corrupted documents.

## What this means practically

The study is not saying "don't use AI agents." It's saying:

1. **Don't set and forget.** Autonomous multi-step workflows without human
   checkpoints will degrade your documents. The longer the chain, the higher the risk.

2. **Audit trails are not optional.** You need to be able to reconstruct what
   changed, when, and why. "It looked right when I checked" is not an audit trail.

3. **The capability is real; the reliability isn't there yet.** Python coding
   works. Complex professional document workflows don't — yet. The researchers
   note models are improving rapidly (GPT family benchmark: 14.7% → 71.5% over
   16 months), so this is a current-state caution, not a permanent ceiling.

4. **The intern analogy holds:** "An intern who destroyed a quarter of a company's
   data during a project would likely be fired, yet businesses are currently
   betting billions on software that does exactly that." We wouldn't let an
   unsupervised intern push changes to a customer installation. Same standard
   applies here.

## Why this is relevant to QuietWire specifically

CAP handles evidence, findings, and attestations — documents that form the basis
of trust decisions for the organizations using it. That's exactly the domain the
study flags as high-risk for agent delegation.

This isn't an argument against using agents in our workflow. It's an argument for:
- Human review checkpoints before anything agent-generated reaches a customer
- Audit trails on any document-modifying operation
- Testing under realistic workflow conditions, not just unit tests
- Not assuming that "it worked in Sana'a" = reproducible and reliable

The #tools-testing-capabilities channel is exactly the right place to develop
these standards. The goal is to build with AI effectively — which requires knowing
where the current limits are.

---

*Shared by Bob Hillery, 20260515*
*Full study: search "DELEGATE-52 Microsoft Research 2026"*
