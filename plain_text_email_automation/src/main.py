import os
import smtplib
from email.mime.text import MIMEText

# Prompt user for email content and recipient
body = input("Enter the body of your email:\n> ")
subject = input("Enter the subject line for your email:\n> ")
target = input("Enter the recipient's email address:\n> ")

# Create the email message
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = os.getenv("GMAIL")  # Sender's email from environment variable
msg["To"] = target  # Recipient's email

# Get sender credentials from environment variables
sender_email = os.getenv("GMAIL")
password = os.getenv("GMAIL_PASSWORD")

# Ensure environment variables are set
if sender_email is None or password is None:
    raise EnvironmentError("GMAIL or GMAIL_PASSWORD environment variables are not set.")

try:
    # Connect to Gmail's SMTP server using TLS
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Start TLS encryption
    server.login(sender_email, password)  # Log in using credentials
    server.send_message(msg)  # Send the email
    print("Email sent successfully.")
except Exception as e:
    # Handle any errors that occur during sending
    print(f"Failed to send email: {e}")
finally:
    # Ensure the server connection is closed
    server.quit()
