"""Extract AAAI keywords — for artificial intelligence and computer science."""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

text = """
We propose a novel transformer architecture with sparse attention mechanisms
for large-scale reinforcement learning. Our approach combines model-based
planning with multi-agent cooperation using graph neural networks and
achieves state-of-the-art performance on continuous control benchmarks.
"""

print("Text:", text.strip())
print()

print("Extracting keywords", end="", flush=True)
keywords = client.keywords(text, n=5, kw_type="aaai")
print(" done\n")
print("AAAI keywords:")
if isinstance(keywords, dict):
    for k, v in keywords.items():
        print(f"  - {k}: {v}")
else:
    for kw in keywords:
        print(f"  - {kw}")

client.close()
