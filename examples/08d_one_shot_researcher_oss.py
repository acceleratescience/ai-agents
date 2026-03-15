"""Run a one-shot researcher task using a self-hosted open-source model.

This example uses gpt-oss-120b, an open-source model served via vLLM
on your own hardware. The model is accessed through an OpenAI-compatible
API endpoint configured via the GPT_OSS_120B_URL environment variable
on the backend.

To use your own OSS model, set on the backend:
  export GPT_OSS_120B_URL="https://your-vllm-server:8443/v1"

The researcher agent produces structured markdown output — no code
execution involved.
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

task = """
Write a brief summary explaining how large language models are trained,
covering pre-training on text corpora, instruction fine-tuning, and
reinforcement learning from human feedback (RLHF). Discuss the main
limitations and open challenges.
"""

print(f"Task:\n{task.strip()}\n")

# Pass the OSS model as both the agent model and the default for all
# supporting agents (controller, formatters, etc.)
result = client.one_shot(
    task=task,
    agent="researcher",
    model="gpt-oss-120b",
    max_rounds=25,
    work_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_one_shot_oss"),
    # These config overrides set the OSS model for all agents:
    defaultModel="gpt-oss-120b",
    defaultFormatterModel="gpt-oss-120b",
)

print(f"\nTask ID:  {result.task_id}")
print(f"Work dir: {result.work_dir}")
print(f"Files:    {[f.path for f in result.files_created]}")
if result.error:
    print(f"Error:    {result.error}")

client.close()
