"""Develop research methods for a quantum error correction project.

Methods generation requires both a data description and an idea to
already exist in the project. This script checks for both and creates
them if missing.

Output files are pulled to output_methods_quantum/ locally.
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
    # local_dir: where project files (idea, methods, etc.) are pulled to locally
    # after each step. The server keeps its own copy; this is your local mirror.
    local_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_methods_quantum"),
)

project_name = "quantum-error-correction"

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

# Try to reuse an existing project
needs_setup = False
try:
    project = client.get_project(project_name)
    print(f"Using existing project: {project_name}\n")

    # Check that data description exists
    try:
        existing_dd = project.get_file("Iteration0/input_files/data_description.md")
        if not existing_dd or len(existing_dd.strip()) == 0:
            raise ValueError("empty")
        print(f"Data description:\n{existing_dd.strip()}\n")
    except Exception:
        print("Data description not found — will recreate project.\n")
        client.delete_project(project_name)
        needs_setup = True

except Exception:
    needs_setup = True

if needs_setup:
    print(f"Data description:\n{data_description.strip()}\n")
    print(f"Creating project: {project_name}")
    project = client.create_project(
        name=project_name,
        data_description=data_description,
    )

# Check that idea exists, generate if missing
try:
    idea_text = project.get_file("Iteration0/input_files/idea.md")
    if not idea_text or len(idea_text.strip()) == 0:
        raise ValueError("empty")
    print(f"Idea:\n{idea_text}\n")
except Exception:
    print("No idea found — generating one first ...")
    idea_text = project.idea()
    print(f"\nIdea:\n{idea_text}\n")

# Generate methods
print("Generating methods (this may take a few minutes) ...")

# Options:
#   default_model  — LLM for methods writer and improver
#   critic_model   — LLM for the reviewers/critics
#
# Example of available models:
#   gemini-3.1-flash-lite-preview, gemini-3.1-pro-preview,
#   gpt-4.1, claude-sonnet-4-6
methods = project.methods(
    default_model="gpt-4.1-2025-04-14",
    critic_model="gemini-3.1-flash-lite-preview",
)

print(f"\n{'='*60}")
print(methods)
print(f"{'='*60}")

print(f"\nOutput files pulled to: {client._local_dir}")

client.close()
