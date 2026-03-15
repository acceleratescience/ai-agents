"""Run a one-shot engineering task: generate and execute code.

The engineer agent writes Python code, runs it locally in an isolated
virtual environment, and returns the results (data files, plots, etc.).

Examples of available models (pass via `model` parameter):
  - gemini-3.1-flash-lite-preview  (fast, cheapest — good default)
  - gemini-3.1-pro-preview         (stronger reasoning)
  - gpt-5-nano                     (fast, good quality)
  - gpt-5.2                        (strongest OpenAI model)
  - claude-sonnet-4-6              (strong all-round)

If `model` is not set, the server default is used.
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

task = """
Generate a synthetic dataset of 500 patients with age, blood pressure,
cholesterol, BMI, and a binary outcome (heart disease yes/no).
Run a logistic regression, print the classification report, and plot
the ROC curve. Save the plot and print the AUC score.
"""

print(f"Task:\n{task.strip()}\n")

result = client.one_shot(
    task=task,
    agent="engineer",
    # model="gpt-5-nano",
    # model="gpt-5.2",
    # model="gemini-3.1-pro-preview",
    # model="claude-sonnet-4-6",
    max_rounds=25,
    max_attempts=3,
    work_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_one_shot_engineer"),
)

print(f"\nTask ID:  {result.task_id}")
print(f"Work dir: {result.work_dir}")
print(f"Files:    {[f.path for f in result.files_created]}")
if result.error:
    print(f"Error:    {result.error}")

client.close()
