"""Generate a research idea for a new project.

This creates a project on the server, runs idea generation, and
prints the result. The idea is also saved on the server and can
be used as input for subsequent pipeline steps (literature, methods, etc.).
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
    local_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_idea"),
)

# The data description grounds the AI in your research context.
# Include: research question, available data, experimental setup,
# hardware/software resources, and any constraints.
data_description = """
We are interested in exploring new approaches to quantum error correction
for near-term noisy intermediate-scale quantum (NISQ) devices.

Context and resources:
- Access to IBM Quantum Experience (ibmq_manila, 5-qubit device)
- Qiskit SDK for circuit design and simulation
- Local workstation with 128GB RAM for classical simulation of up to 20 qubits
- Noise models extracted from real device calibration data
- Goal: develop error mitigation strategies that work within current hardware limitations
"""

print(f"Data description:\n{data_description.strip()}\n")

project = client.create_project(
    name="quantum-error-correction",
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
    default_model="claude-sonnet-4-6",
    critic_model="gemini-3.1-flash-lite-preview",
    idea_iterations=3,
)

print(f"\n{'='*60}")
print(idea)
print(f"{'='*60}")

client.close()
