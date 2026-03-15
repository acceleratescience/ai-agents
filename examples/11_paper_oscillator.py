"""Write a paper from an existing project that already has idea, literature, methods, and results.

This script reuses the harmonic-oscillator project created by 10_pipeline_oscillator.py.
It checks that all required inputs exist before generating the paper.

Output files (LaTeX) are pulled to output_paper_oscillator/ locally.
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
    # local_dir: where project files are pulled to locally after each step.
    local_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_paper_oscillator"),
)

project_name = "harmonic-oscillator"

# Get existing project
try:
    project = client.get_project(project_name)
    print(f"Using existing project: {project_name}\n")
except Exception:
    print(f"ERROR: Project '{project_name}' not found. Run 10_pipeline_oscillator.py first.")
    client.close()
    exit(1)

# Verify all required inputs exist
required_files = {
    "Data description": "Iteration0/input_files/data_description.md",
    "Idea": "Iteration0/input_files/idea.md",
    "Methods": "Iteration0/input_files/methods.md",
    "Results": "Iteration0/input_files/results.md",
}

for label, path in required_files.items():
    try:
        content = project.get_file(path)
        if not content or len(content.strip()) == 0:
            raise ValueError("empty")
        print(f"{label}: found ({len(content):,} chars)")
    except Exception:
        print(f"ERROR: {label} not found at {path}. Run earlier pipeline steps first.")
        client.close()
        exit(1)

# Generate paper
print("\nWriting paper (this may take several minutes) ...")

# Options:
#   journal        — target journal for formatting (e.g. "AAS", "MNRAS", "NONE")
#   add_citations  — include bibliography from literature search
#   default_model  — LLM for paper writing (needs a capable model for structured output)
#   timeout        — max seconds to wait (paper writing can be slow)
#
# Note: paper writing requires reliable structured JSON output, so use a
# capable model (gemini-3.1-pro-preview or better). Flash-lite may fail.
#
# Examples of available models:
#   gemini-3.1-pro-preview, gpt-5-nano, gpt-5.2, claude-sonnet-4-6
paper = project.paper(
    journal="AAS",
    add_citations=True,
    default_model="gemini-2.5-flash",
    timeout=1000,
)

print(f"\n{'='*60}")
print(f"Paper generated ({len(paper):,} chars of LaTeX)")
print(f"{'='*60}")
print(paper[:1000])
print("...")

# Pull all files including the paper
project.pull_files()

print(f"\nOutput files pulled to: {client._local_dir}")

client.close()
