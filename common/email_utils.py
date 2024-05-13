import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Now you can access the variables
from_email = os.getenv('FROM_EMAIL')
email_pw = os.getenv('EMAIL_PW')
to_email = os.getenv('TO_EMAIL')
email_host = os.getenv('EMAIL_HOST')
email_port = os.getenv('EMAIL_PORT')

def send_email(subject, body, to_address = to_email, from_address = from_email, smtp_server = email_host, smtp_port = email_port, smtp_username = from_email, smtp_password = email_pw):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(smtp_username, smtp_password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()