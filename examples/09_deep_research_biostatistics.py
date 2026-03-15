"""Run a deep research task in biostatistics with planning and multi-step execution.

Deep research orchestrates a planning phase (planner + reviewer) followed by
step-by-step execution with specialised agents. Code runs locally in an
isolated virtual environment.

This example uses a 2-step plan:
  1. Engineer: generate synthetic clinical trial data and run survival analysis
  2. Researcher: interpret the results and write a data guide

Models can be set per-agent. Here we use:
  - gpt-oss-120b for the researcher (self-hosted open-source model)
  - gemini-3.1-flash-lite-preview for the engineer and all other agents

Examples of available models:
  - gemini-3.1-flash-lite-preview  (fast, cheapest)
  - gemini-3.1-pro-preview         (stronger reasoning)
  - gpt-5-nano                     (fast, good quality)
  - gpt-5.2                        (strongest OpenAI model)
  - claude-sonnet-4-6              (strong all-round)
  - gpt-oss-120b                   (self-hosted, free)
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

task = """
We have a randomised controlled trial (RCT) dataset with 400 patients
(200 treatment, 200 control) followed over 24 months. Variables include
age, sex, baseline biomarker level, treatment arm, time-to-event, and
event indicator (death or disease progression).

1. Generate realistic synthetic survival data with these characteristics.
   Fit a Cox proportional hazards model and produce:
   - Kaplan-Meier survival curves by treatment arm
   - Forest plot of hazard ratios for all covariates
   - A table of model coefficients with confidence intervals

2. Write a data guide interpreting the results: discuss statistical
   significance, clinical relevance of the hazard ratios, any
   violations of the proportional hazards assumption, and
   recommendations for follow-up analyses.
"""

print(f"Task:\n{task.strip()}\n")

result = client.deep_research(
    task=task,

    # Planning configuration
    max_plan_steps=2,
    n_plan_reviews=1,
    plan_instructions="1. engineer, 2. researcher.",

    # Per-agent model overrides
    engineer_model="gemini-3.1-flash-lite-preview",
    researcher_model="gpt-oss-120b",

    # Control configuration
    max_rounds=100,
    max_attempts=3,

    # Execution
    work_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_deep_research_biostat"),
)

print(f"\nTask ID:  {result.task_id}")
print(f"Work dir: {result.work_dir}")
print(f"Files:    {[f.path for f in result.files_created]}")
if result.error:
    print(f"Error:    {result.error}")

client.close()
