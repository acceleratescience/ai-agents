"""Generate a research idea for a chemical engineering project."""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
    local_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_idea_chemeng"),
)

# The data description grounds the AI in your research context.
# Include: research question, available data, experimental setup,
# hardware/software resources, and any constraints.
data_description = """
We want to optimise a continuous-flow microreactor for the synthesis of
biodegradable polyesters from lactic acid. The goal is to maximise
monomer conversion while minimising energy consumption and byproduct
formation.

Context and resources:
- Syrris Asia continuous-flow microreactor system (0.5-10 mL/min flow rates)
- In-line FTIR (ReactIR) and UV-Vis for real-time reaction monitoring
- GPC (gel permeation chromatography) for polymer molecular weight distribution
- DSC and TGA for thermal characterisation of product
- Design of experiments (DoE) framework: temperature (120-200°C), residence time (5-60 min), catalyst loading (0.1-2 wt%)
- Process simulation in Aspen Plus, kinetic modelling in Python (scipy, cantera)
- Pilot-scale validation in 50L batch reactor available for promising candidates
"""

print(f"Data description:\n{data_description.strip()}\n")

project = client.create_project(
    name="microreactor-polyester",
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
