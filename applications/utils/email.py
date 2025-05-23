import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

def send_basic_email(subject,message,to_email):
    load_dotenv()

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(os.getenv("EMAIL_HOST_USER"), 'hpkb cgru yhlk jrgi')

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = os.getenv("EMAIL_HOST_USER")
        msg['To'] = to_email
        msg.set_content(message)

        smtp.send_message(msg)