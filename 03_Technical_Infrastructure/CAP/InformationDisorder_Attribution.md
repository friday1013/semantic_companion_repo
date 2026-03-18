# Information Disorder — Mis, Dis, and Malinformation

## The Diagram

The Venn diagram included in this package (`WardleOIP-66109306.jpg`)
illustrates the three-part taxonomy of information disorder:

- **Misinformation** — false information that spreads *regardless of intent* to mislead
- **Disinformation** — *deliberately* created to harm, manipulate, or mislead
- **Malinformation** — based on fact but taken out of context *to mislead, harm, or manipulate*

## Attribution

**Original framework:** Claire Wardle and Hossein Derakhshan  
**Original publication:** *Information Disorder: Toward an Interdisciplinary Framework
for Research and Policy*, Council of Europe Report DGI(2017)09, 2017  
**Publisher:** First Draft (firstdraftnews.org), commissioned by the Council of Europe  
**First published:** February 2017

The diagram in this package is the CISA / First Draft version, widely reproduced
under the original framework. The intellectual origin and taxonomy are Wardle &
Derakhshan's. Claire Wardle is co-founder of First Draft and the leading scholar
on information disorder; Hossein Derakhshan is a researcher and journalist.

**Canonical citation:**
> Wardle, C. and Derakhshan, H. (2017). *Information Disorder: Toward an
> interdisciplinary framework for research and policy.* Council of Europe report
> DGI(2017)09. Strasbourg: Council of Europe.

Available at: https://firstdraftnews.org/long-form-article/understanding-information-disorder/

## Why This Matters for CAP and NIDP

NIDP (Narrative Integrity Distribution Protocol) is designed to operate across
all three categories of information disorder — not just deliberate disinformation.

- **Misinformation** is addressed through provenance attestation: a node can trace
  *where* a narrative originated and *who* vouched for it, catching false information
  even when the spreader was acting in good faith.

- **Disinformation** is addressed through the NIDP threat scoring and precision
  modes: ThreatScore >= 0.8 triggers Iron Canon, preventing narrative drift under
  active adversarial campaigns.

- **Malinformation** is the hardest category and the most important. Genuine facts
  taken out of context are nearly invisible to content-based detection. Provenance
  attestation and canonical context anchoring — the core of NIDP — are the primary
  defense: not "is this true?" but "is this the authorized context for this truth?"

This is why the NIDP framework was designed around *attestation* rather than
*fact-checking*. Facts can be weaponized. Provenance chains are harder to fake.
