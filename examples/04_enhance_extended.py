#!/usr/bin/env python3
"""Enhance a task description with context from referenced papers.

The enhance tool fetches and summarises papers referenced in the input
text, producing enriched text that gives AI agents much better context
to work with. This is useful as a preprocessing step before submitting
tasks for analysis.

Supported sources:
  - arXiv URLs
  - bioRxiv / medRxiv URLs
  - PubMed / PMC URLs
  - Generic PDF links (e.g. journal papers)
  - Loose bibliographic references (e.g. "Smith et al. 2020"),
    resolved to arXiv papers via Skepthical
"""

import os

import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
    timeout=3000
)

text = """
  We investigate the role of immune checkpoint inhibitors in treating
  non-small cell lung cancer (NSCLC). Our approach builds on the landmark
  clinical trial results from https://arxiv.org/abs/2312.08517 and the
  tumor microenvironment profiling described in
  https://www.biorxiv.org/content/10.1101/2024.02.13.580055v1.

  We also incorporate single-cell RNA sequencing data from
  https://pubmed.ncbi.nlm.nih.gov/35121771/ to characterize T-cell
  exhaustion signatures. The PD-1/PD-L1 pathway analysis follows
  Topalian et al. (2012) and the combination therapy framework of
  Hellmann & Rizvi (2018). For the statistical methodology we refer
  to Benjamini and Hochberg (1995).
"""

print(f"Input:\n{text.strip()}\n")
print("Enhancing (this may take a minute) ...")

# Options:
#   max_workers         — parallel download workers (default 2)
#   max_depth           — max summarisation depth (default 10)
#   resolve_references  — resolve loose refs like "Smith et al. 2020" (default True)
#   max_references      — max loose references to resolve (default 10)
enhanced = client.enhance(text)

print(f"\nEnhanced text:\n{enhanced}")

client.close()