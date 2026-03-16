"""Generate literature review for a marine biology project on coral bleaching.

Literature generation requires both a data description and an idea to
already exist in the project. This script checks for both and creates
them if missing.

Output files are pulled to output_literature_coral/ locally.
"""

import os
import air

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
    # local_dir: where project files (idea, literature, etc.) are pulled to locally
    # after each step. The server keeps its own copy; this is your local mirror.
    local_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_literature_coral"),
)

project_name = "coral-bleaching-study"

# The data description grounds the AI in your research context.
# Include: research question, available data, experimental setup,
# hardware/software resources, and any constraints.
data_description = """
We have 15 years of coral bleaching data from the Great Barrier Reef,
including sea surface temperature records, coral species composition,
bleaching severity scores, and recovery rates across 150 reef sites.

Context and resources:
- Satellite SST data (NOAA Coral Reef Watch, 2008-2023)
- Field surveys: bleaching severity and species abundance (biannual)
- Underwater photoquadrat imagery for percent cover estimation
- Environmental covariates: wave exposure, turbidity, depth, proximity to river plumes
- Analysis in Python (xarray, scikit-learn) and R (mgcv for GAMs)
- Goal: predict future bleaching events and identify resilient reef sites
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

# Generate literature review
print("Generating literature review (this may take a few minutes) ...")

# Options:
#   default_model — LLM for literature search and synthesis
#   timeout       — max seconds to wait (default 600, literature can be slow)
#   max_iterations - how many times Semantic Scholar is called
literature = project.literature(timeout=900, max_iterations=10)

print(f"\n{'='*60}")
print(literature)
print(f"{'='*60}")

print(f"\nOutput files pulled to: {client._local_dir}")

client.close()
