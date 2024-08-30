import os

# Directorios a crear
directories = [
    "connections",
    "prompts",
    "scripts",
    "utils"
]

# Archivos y sus contenidos
files = {
    "main.py": '''from scripts.diff_to_commit import diff_to_commit_message

if __name__ == "__main__":
    ticket_number = input("Enter the ticket number: ")
    diff_to_commit_message(ticket_number)
''',

    "prompts/diff_to_commit_msg_prompt.py": '''DIFF_TO_COMMIT_MSG_PROMPT = """Given the following diff, generate a conventional commit message (with type, scope, description, body).
The title should follow the format '<emoji> <type>(%s): <description>' or ':rotating_light: <type>(%s)!: <description>' for breaking changes.
Write it in simple English and in a markdown formatted text block without using triple backticks, except for the first and last.

Use the appropriate emoji based on the commit type:
- feat: :sparkles:
- fix: :bug:
- docs: :books:
- style: :gem:
- refactor: :hammer:
- perf: :rocket:
- test: :white_check_mark:
- build: :package:
- ci: :construction_worker:
- chore: :wrench:
- breaking changes: :rotating_light:
(the breaking changes emoji gains priority over the others, and adds a ! symbol before de colon)

Examples:

"""
''',

    "prompts/commit_message_example.py": '''COMMIT_MESSAGE_EXAMPLE = """:sparkles: feat(ATM-120): complete WorkstreamStatus component and add new status icons

- Finalized the implementation of the WorkstreamStatus component:
  - Added dynamic workstream selection
  - Displayed workstream statuses
  - Implemented detailed view for each workstream
- Added new SVG icons for various statuses:
  - done
  - undone
- Removed an unused import from the Snackbar component"
'''
,

    "scripts/diff_to_commit.py": '''import subprocess
from utils import logging, project_prefix
from prompts.diff_to_commit_msg_prompt import DIFF_TO_COMMIT_MSG_PROMPT
from prompts.commit_message_example import COMMIT_MESSAGE_EXAMPLE

def diff_to_commit_message(ticket: str):
    if not ticket:
        logging.log_error("Please provide a ticket number.")
        return
    
    logging.log("Ensuring ticket prefix...")
    ticket = project_prefix.ensure_prefix(ticket)

    logging.log("Generating diff...")
    result = subprocess.run(["git", "diff", "--staged", "--unified=2"], capture_output=True, text=True)
    diff = result.stdout

    if not diff:
        logging.log_warning("No changes staged for commit. Please stage your changes first.")
        return

    prompt = f"For ticket {ticket}. {DIFF_TO_COMMIT_MSG_PROMPT}\\n{COMMIT_MESSAGE_EXAMPLE}\\n\\n---\\n\\n{diff}"

    logging.log("Copying commit message prompt to clipboard...")
    subprocess.run("echo '{}' | clip".format(prompt.replace('\"', '\\\"')), shell=True)

    logging.log_success("The commit message prompt has been copied to the clipboard. You can ask an AI to generate the commit message from it.")
'''
,

    "utils/__init__.py": "",
    
    "utils/logging.py": '''def log(message):
    print(f"\\033[1;34m{message}\\033[0m")

def log_warning(message):
    print(f"\\033[1;33m{message}\\033[0m")

def log_error(message):
    print(f"\\033[1;31m{message}\\033[0m")

def log_success(message):
    print(f"\\033[1;32m{message}\\033[0m")
''',

    "utils/project_prefix.py": '''import subprocess

def get_project_prefix():
    result = subprocess.run(["git", "config", "--get", "jira.project"], capture_output=True, text=True)
    return result.stdout.strip() + "-"

def ensure_prefix(ticket: str):
    project_prefix = get_project_prefix()
    if not ticket.startswith(project_prefix):
        ticket = f"{project_prefix}{ticket}"
    return ticket
'''
}

# Crear directorios
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Crear archivos con contenidos
for filepath, content in files.items():
    with open(filepath, 'w') as file:
        file.write(content)

print("Estructura creada exitosamente.")
