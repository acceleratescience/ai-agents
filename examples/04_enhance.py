"""Enhance a task description with context from arXiv papers.

When you reference arXiv papers in a task, the enhance tool fetches and
summarises them, producing enriched text that gives AI agents much better
context to work with. This is useful as a preprocessing step before
submitting tasks for analysis.
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

text = """
We want to implement the variational quantum eigensolver (VQE) described
in https://arxiv.org/abs/1304.3061 to estimate the ground state energy
of small molecules. We will compare with the quantum approximate
optimization algorithm (QAOA) from https://arxiv.org/abs/1411.4028
on a set of combinatorial benchmark problems.
"""

print(f"Input:\n{text.strip()}\n")
print("Enhancing (this may take a minute) ...")

enhanced = client.enhance(text)

print(f"\nEnhanced text:\n{enhanced}")

client.close()
