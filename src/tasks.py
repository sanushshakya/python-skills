from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import get_settings

# Initialize Celery app with Redis as the broker and result backend
celery_app = Celery(
    __name__,
    broker=get_settings().CELERY_BROKER_URL,
    backend=get_settings().CELERY_RESULT_BACKEND,
)

# Function to send an email
def send_email(subject: str, recipient: str, body: str):
    settings = get_settings()
    sender = settings.EMAIL_SENDER
    password = settings.EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(settings.EMAIL_SERVER, settings.EMAIL_PORT)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, recipient, text)
    server.quit()

# Celery task to send a welcome email
@celery_app.task(name="send_welcome_email")
def send_welcome_email(user_email: str):
    """
    Sends a welcome email to the user.
    
    Args:
        user_email (str): The email address of the user to receive the welcome email.
    """
    subject = "Welcome to Our Service!"
    body = f"Hello! Thank you for registering with us. We are excited to have you on board."
    
    # Call the send_email function to send the email
    send_email(subject, user_email, body)