import subprocess

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from prompts.commit_message_example import COMMIT_MESSAGE_EXAMPLE
from prompts.diff_to_commit_msg_prompt import DIFF_TO_COMMIT_MSG_PROMPT
from utils import logging, project_prefix


def diff_to_commit_message(ticket: str):
    if not ticket:
        logging.log_error("Please provide a ticket number.")
        return

    logging.log("Ensuring ticket prefix...")
    ticket = project_prefix.ensure_prefix(ticket)

    logging.log("Staging changes with 'git add'...")
    subprocess.run(["git", "add", "."], check=True)

    logging.log("Generating diff...")
    result = subprocess.run(["git", "diff", "--staged", "--unified=2"], capture_output=True, text=True)
    diff = result.stdout

    if not diff:
        logging.log_warning("No changes staged for commit. Please stage your changes first.")
        return

    prompt_template = f"For ticket {ticket}. {DIFF_TO_COMMIT_MSG_PROMPT}\n{COMMIT_MESSAGE_EXAMPLE}\n\n---\n\n{diff}"

    logging.log("Generating commit message using LangChain...")

    # Set up LangChain to use OpenAI
    llm = OpenAI(temperature=0.7)  # Adjust 'temperature' based on desired outcome
    prompt = PromptTemplate(template=prompt_template, input_variables=[])
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain to generate the commit message
    commit_message = chain.run({})

    logging.log_success(f"Generated Commit Message:\n{commit_message}")

    # You can add code here to copy the message to the clipboard if needed
