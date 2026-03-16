#!/usr/bin/env python3
"""Review a paper PDF with the Skepthical engine.

Two examples:
  - Review a paper downloaded from arXiv
  - Review a local PDF file

The review report is saved locally as both markdown and PDF files.
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

# --- Option A: review a paper from arXiv ---
arxiv_url = "https://arxiv.org/abs/1706.03762"  # "Attention Is All You Need"
print(f"Downloading {arxiv_url} ...")
arxiv_result = client.arxiv(arxiv_url)
pdf_path = arxiv_result["downloaded_files"][0]

# --- Option B: review a local PDF ---
# pdf_path = "localpaper.pdf"

print(f"Paper: {pdf_path}")

# Options:
#   thoroughness       — "Standard" (single reviewer) or "High" (two merged)
#   figures_review     — detailed figure/diagram analysis
#   verify_statements  — cross-check claims against references
#   review_maths       — audit mathematical derivations
#   review_numerics    — audit numerical computations
#   emails             — send the finished report to these addresses
#   timeout            — max seconds to wait (default 3600)

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_review")

print("\nRunning Skepthical review (this may take a few minutes) ...")

review_result = client.review(
    pdf_path,
    output_dir=output_dir,
    thoroughness="Standard",
    figures_review=False,
    verify_statements=False,
    review_maths=False,
    review_numerics=False,
    # emails=["you@example.com"],  # optional: receive the report by email
    timeout=3600,
)

print(f"\n{'='*60}")
print(f"Markdown: {review_result['review_md_path']}")
print(f"PDF:      {review_result['review_pdf_path'] or '(not available)'}")
print(f"{'='*60}")
print(review_result["review"])

client.close()
