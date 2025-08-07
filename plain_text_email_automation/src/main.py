import os
import smtplib
from email.mime.text import MIMEText

body = input("Enter the body of your email:\n> ")
subject = input("Enter the subject line for your email:\n> ")
target = input("Enter the recipient's email address:\n> ")

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = os.getenv("GMAIL")
msg["To"] = target

sender_email = os.getenv("GMAIL")
password = os.getenv("GMAIL_PASSWORD")

if sender_email is None or password is None:
    raise EnvironmentError("GMAIL or GMAIL_PASSWORD environment variables are not set.")

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.send_message(msg)
    print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()