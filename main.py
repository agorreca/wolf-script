from scripts.diff_to_commit import diff_to_commit_message

if __name__ == "__main__":
    ticket_number = input("Enter the ticket number: ")
    diff_to_commit_message(ticket_number)
