"""Upload a local PDF and extract its full text with OCR.

Place a file called localpaper.pdf in the same directory as this script.
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

local_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "localpaper.pdf")
if not os.path.exists(local_pdf):
    print(f"Please place a PDF at: {local_pdf}")
    exit(1)

print(f"Local PDF: {local_pdf}")

# Step 1: Upload to a temporary project
project = client.create_project("ocr-temp")
project.push_files(local_pdf, remote_path="docs/localpaper.pdf")
print("Uploaded to server.")

# Step 2: Get the server-side path
info = client._client.get(f"/api/v1/projects/ocr-temp").json()
server_pdf = os.path.join(info["project_dir"], "docs", "localpaper.pdf")
print(f"Server path: {server_pdf}")

# Step 3: Run OCR
print("\nRunning OCR ...")
ocr_result = client.ocr(server_pdf)

full_text = ocr_result.get("full_text", "")
full_markdown = ocr_result.get("full_markdown", "")

print(f"Extracted {len(full_text):,} characters (text), {len(full_markdown):,} characters (markdown)")
print(f"\n--- First 500 chars ---\n{full_text[:500]}")

# Step 4: Save markdown locally
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ocr_output")
os.makedirs(output_dir, exist_ok=True)
md_path = os.path.join(output_dir, "localpaper.md")
with open(md_path, "w") as f:
    f.write(full_markdown)
print(f"\nMarkdown saved to: {md_path}")

# Cleanup
client.delete_project("ocr-temp")
client.close()
