"""Extract UNESCO keywords — works for any academic discipline."""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

text = """
Adenosine triphosphate (ATP) is the primary energy currency of all
living cells, providing energy for metabolic processes via hydrolysis
of high-energy phosphodiester bonds. ATP powers active transport,
muscle contraction, and biosynthesis.
"""

print("Text:", text.strip())
print()

print("Extracting keywords", end="", flush=True)
keywords = client.keywords(text, n=5, kw_type="unesco")
print(" done\n")
print("UNESCO keywords:")
for kw in keywords:
    print(f"  - {kw}")

client.close()
