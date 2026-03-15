"""Extract AAS (American Astronomical Society) keywords — for astronomy & astrophysics."""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

text = """
We study cosmic microwave background anisotropies and their implications
for dark energy models using Bayesian inference and MCMC methods to
constrain cosmological parameters from Planck data combined with
baryon acoustic oscillation measurements and Type Ia supernovae.
"""

print("Text:", text.strip())
print()

print("Extracting keywords", end="", flush=True)
keywords = client.keywords(text, n=5, kw_type="aas")
print(" done\n")
print("AAS keywords:")
if isinstance(keywords, dict):
    for k, v in keywords.items():
        print(f"  - {k}: {v}")
else:
    for kw in keywords:
        print(f"  - {kw}")

client.close()
