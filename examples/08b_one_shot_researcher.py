"""Run a one-shot researcher task: generate a written analysis or report.

The researcher agent produces structured markdown output — no code
execution involved. Ideal for literature reviews, data interpretation,
writing guides, or any task that requires reasoning and writing rather
than computation.

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
Write a 500-word comparative analysis of three major ethical frameworks
(utilitarianism, deontological ethics, virtue ethics) and how they apply
to the question of AI-generated content in academic publishing.
Discuss the tensions between efficiency gains and academic integrity.
"""

print(f"Task:\n{task.strip()}\n")

result = client.one_shot(
    task=task,
    agent="researcher",
    # model="gpt-5-nano",
    # model="gpt-5.2",
    # model="gemini-3.1-pro-preview",
    # model="claude-sonnet-4-6",
    max_rounds=25,
    work_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_one_shot_researcher"),
)

print(f"\nTask ID:  {result.task_id}")
print(f"Work dir: {result.work_dir}")
print(f"Files:    {[f.path for f in result.files_created]}")
if result.error:
    print(f"Error:    {result.error}")

client.close()
