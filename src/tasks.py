"""
src/tasks.py
This file contains Celery tasks for handling background operations in the User Management API.
"""

from celery import shared_task
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@shared_task
def send_password_reset_email(user_email, reset_token):
    """
    Send a password reset email to the user.

    Args:
        user_email (str): The email address of the user.
        reset_token (str): The token used for resetting the password.
    """

    # Email credentials and server details
    sender_email = "your_email@example.com"
    receiver_email = user_email
    password = "your_email_password"

    # Create the container email message.
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Password Reset Request"

    # Email body content
    reset_url = f"http://localhost:8000/reset-password?token={reset_token}"
    body = f"Hello, to reset your password, please visit the following link:\n{reset_url}"

    # Attach the email body with the MIMEText object
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

    except Exception as e:
        raise Exception(f"Failed to send email: {e}")