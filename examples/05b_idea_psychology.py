"""Generate a research idea for a psychology project."""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
    local_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_idea_psychology"),
)

# The data description grounds the AI in your research context.
# Include: research question, available data, experimental setup,
# hardware/software resources, and any constraints.
data_description = """
We study the effect of social media usage on adolescent mental health,
focusing on anxiety and self-esteem. We want to design a longitudinal
study that disentangles correlation from causation.

Context and resources:
- Access to a cohort of 500 high-school students (ages 14-18) with parental consent
- Validated psychometric instruments: GAD-7 (anxiety), Rosenberg Self-Esteem Scale
- Screen-time tracking via Digital Wellbeing API (Android) and Screen Time API (iOS)
- Experience sampling methodology (ESM) via custom smartphone app (5 prompts/day)
- Ethics approval from university IRB, GDPR-compliant data handling
- Statistical analysis in R (lavaan for SEM, lme4 for mixed-effects models)
"""

print(f"Data description:\n{data_description.strip()}\n")

project = client.create_project(
    name="social-media-mental-health",
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
