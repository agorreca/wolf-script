import subprocess

def get_project_prefix():
    result = subprocess.run(["git", "config", "--get", "jira.project"], capture_output=True, text=True)
    return result.stdout.strip() + "-"

def ensure_prefix(ticket: str):
    project_prefix = get_project_prefix()
    if not ticket.startswith(project_prefix):
        ticket = f"{project_prefix}{ticket}"
    return ticket
