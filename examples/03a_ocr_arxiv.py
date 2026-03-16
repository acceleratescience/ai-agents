"""Download a paper from arXiv and extract its full text with OCR.

The OCR returns both plain text and markdown. The markdown version
preserves structure (headings, equations, tables) and can be saved locally.
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

# Step 1: Download paper from arXiv (a machine learning paper)
arxiv_url = "https://arxiv.org/abs/1706.03762"  # "Attention Is All You Need"
print(f"Downloading {arxiv_url} ...")

arxiv_result = client.arxiv(arxiv_url)
print(f"Downloads: {arxiv_result.get('downloads_successful', 0)} successful")

pdf_path = arxiv_result["downloaded_files"][0]
print(f"PDF on server: {pdf_path}")

# Step 2: Run OCR on the downloaded PDF
print(f"\nRunning OCR ...")
ocr_result = client.ocr(pdf_path)

full_text = ocr_result.get("full_text", "")
full_markdown = ocr_result.get("full_markdown", "")

print(f"Extracted {len(full_text):,} characters (text), {len(full_markdown):,} characters (markdown)")
print(f"\n--- First 500 chars (text) ---\n{full_text[:500]}")

# Step 3: Save markdown locally
output_dir = os.path.join(os.path.dirname(__file__), "ocr_output")
os.makedirs(output_dir, exist_ok=True)
md_path = os.path.join(output_dir, "attention_is_all_you_need.md")
with open(md_path, "w") as f:
    f.write(full_markdown)
print(f"\nMarkdown saved to: {md_path}")

client.close()
