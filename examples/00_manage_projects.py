"""List and delete projects on the server."""

import os
import sys
import air

HELP = """
Usage:
  python 00_manage_projects.py              List all projects
  python 00_manage_projects.py delete NAME  Delete a project
  python 00_manage_projects.py delete-all   Delete all projects (asks confirmation)
  python 00_manage_projects.py --help       Show this message
""".strip()

if "--help" in sys.argv or "-h" in sys.argv:
    print(HELP)
    sys.exit(0)

client = air.AIR(
    api_key=os.environ["AIR_API_KEY"],
    base_url=os.environ.get("AIR_BASE_URL", "http://localhost:8000"),
)

# List all projects
projects = client.list_projects()
print(f"Projects on server ({len(projects)}):")
for p in projects:
    print(f"  - {p}")

# Delete all projects
if len(sys.argv) >= 2 and sys.argv[1] == "delete-all":
    confirm = input(f"\nDelete all {len(projects)} projects? (yes/no): ")
    if confirm.strip().lower() == "yes":
        for p in projects:
            print(f"  Deleting {p} ...", end="")
            client.delete_project(p)
            print(" done")
        print("All projects deleted.")
    else:
        print("Cancelled.")

# Delete a single project
elif len(sys.argv) >= 3 and sys.argv[1] == "delete":
    name = sys.argv[2]
    print(f"\nDeleting project: {name}")
    client.delete_project(name)
    print("Deleted.")

client.close()
