from common.email_utils import send_email

# Open the log file and read its contents
with open('/app/app.log', 'r') as file:
    log_contents = file.read()

# Send the email with the log contents as the body
send_email("Tracker Automation - Successful Execution", log_contents)