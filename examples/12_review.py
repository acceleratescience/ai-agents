#!/usr/bin/env python3
"""Review a paper PDF with the Skepthical engine.

This downloads a paper from arXiv, then runs a standalone Skepthical
review on it. The review report is saved locally as both markdown and
PDF files.

Alternatively, you can point directly at a PDF already on the server
(see the commented-out section below).
"""

import os
import sys

import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

# ── 1. Get a paper PDF on the server ───────────────────────────────
#
# Option A: point to a PDF that already exists on the server.
# pdf_path = "/path/on/server/to/paper.pdf"
#
# Option B: download from arXiv (used by default below).

arxiv_url = "https://arxiv.org/abs/1105.3470"
print(f"Downloading paper from {arxiv_url} ...")

arxiv_result = client.arxiv(arxiv_url)
downloaded = arxiv_result.get("downloaded_files", [])
if not downloaded:
    client.close()
    sys.exit("No PDF was downloaded — check the arXiv URL.")

pdf_path = downloaded[0]
print(f"PDF on server: {pdf_path}\n")

# ── 2. Run a Skepthical review ─────────────────────────────────────
#
# Options:
#   thoroughness       — "Standard" (single reviewer) or "High" (two merged)
#   figures_review     — detailed figure/diagram analysis
#   verify_statements  — cross-check claims against references
#   review_maths       — audit mathematical derivations
#   review_numerics    — audit numerical computations
#   emails             — send the finished report to these addresses
#   timeout            — max seconds to wait (default 3600)
#   poll_interval      — seconds between status polls (default 5)

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_review")

print("Running Skepthical review (this may take a few minutes) ...")

review_result = client.review(
    pdf_path,
    output_dir=output_dir,
    thoroughness="Standard",
    figures_review=False,
    verify_statements=False,
    review_maths=False,
    review_numerics=False,
    timeout=600,
    poll_interval=5.0,
)

print(f"\n{'='*60}")
print(f"Markdown: {review_result['review_md_path']}")
print(f"PDF:      {review_result['review_pdf_path'] or '(not available)'}")
print(f"{'='*60}")
print(review_result["review"])

client.close()
