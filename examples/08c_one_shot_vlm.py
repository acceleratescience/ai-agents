"""Run a one-shot engineering task with VLM (vision) feedback on plots.

When enable_vlm_review=True, after the engineer generates a plot, a
vision-language model reviews the image and provides feedback. If the
plot needs improvement, the engineer revises and re-runs the code
automatically — up to max_vlm_review_attempts times.

Examples of available models for the engineer (pass via `model` parameter):
  - gemini-3.1-flash-lite-preview  (fast, cheapest — good default)
  - gemini-3.1-pro-preview         (stronger reasoning)
  - gpt-5-nano                     (fast, good quality)
  - gpt-5.2                        (strongest OpenAI model)
  - claude-sonnet-4-6              (strong all-round)

The VLM reviewer model defaults to gemini-3.1-flash-image-preview
(a vision-capable model). You can override it with vlm_model=...
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

task = """
Plot a 2D phase space diagram of the Lorenz attractor.
Use scipy to integrate the Lorenz system with parameters sigma=10, rho=28, beta=8/3.
Make the plot publication-quality with a colorbar showing time evolution.
"""

print(f"Task:\n{task.strip()}\n")

result = client.one_shot(
    task=task,
    agent="engineer",
    # model="gpt-5-nano",
    # model="gpt-5.2",
    # model="gemini-3.1-pro-preview",
    # model="claude-sonnet-4-6",
    enable_vlm_review=True,
    max_vlm_review_attempts=3,
    max_rounds=25,
    max_attempts=3,
    work_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_one_shot_vlm"),
)

print(f"\nTask ID:  {result.task_id}")
print(f"Work dir: {result.work_dir}")
print(f"Files:    {[f.path for f in result.files_created]}")
if result.error:
    print(f"Error:    {result.error}")

client.close()
