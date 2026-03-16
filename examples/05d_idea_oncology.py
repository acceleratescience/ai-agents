"""Generate a research idea for a cancer biology/oncology project."""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
    local_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_idea_oncology"),
)

# The data description grounds the AI in your research context.
# Include: research question, available data, experimental setup,
# hardware/software resources, and any constraints.
data_description = """
We want to investigate the role of chromothripsis-driven genome
rearrangements in drug resistance in colorectal cancer. Specifically,
we aim to use CRISPR-based functional genomics to identify which
rearrangements are driver events and which are passengers.

Context and resources:
- Patient-derived organoids (PDOs) from a biobank of 50 colorectal cancer patients
- CRISPR genome editing capability: Cas9, Cas12a, prime editing, base editing
- Genome-scale CRISPR knockout and activation libraries
- Patient-derived xenograft (PDX) models for in vivo validation
- Sequencing: Illumina NovaSeq X Plus (bulk WGS/RNA-seq), 10X Genomics
  Chromium for single-cell RNA-seq, spatial transcriptomics (Visium)
- Long-read sequencing (Oxford Nanopore PromethION) for structural variant detection
- Bioinformatics HPC cluster with standard cancer genomics pipelines
- Drug screening: automated liquid handling for high-throughput viability assays
"""

print(f"Data description:\n{data_description.strip()}\n")

project = client.create_project(
    name="chromothripsis-drug-resistance",
    data_description=data_description,
)

print("Generating idea (this may take a minute) ...")

# Options:
#   default_model    — LLM for idea generation (sampler, selector, maker)
#   critic_model     — LLM for the idea critic
#   idea_iterations  — maker <-> critic rounds (default 3)
#
# Example of available models:
#   gemini-3.1-flash-lite-preview, gemini-3.1-pro-preview,
#   gpt-4.1, claude-sonnet-4-6
idea = project.idea(
    default_model="gpt-4.1-2025-04-14",
    critic_model="gemini-3.1-pro-preview",
    idea_iterations=3,
)

print(f"\n{'='*60}")
print(idea)
print(f"{'='*60}")

client.close()
