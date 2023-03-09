import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, body):
    """
    Sends an email using SMTP and the email library.

    Parameters:
        sender_email (str): The email address of the sender.
        sender_password (str): The password of the sender's email account.
        recipient_email (str): The email address of the recipient.
        subject (str): The subject line of the email.
        body (str): The body of the email.

    Returns:
        None
    """

    email_to = ', '.join(recipient_email)

    # Create a message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email_to
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Log into email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(sender_email, sender_password)

    # Send email
    text = message.as_string()
    server.sendmail(sender_email, recipient_email, text)

    # Close the connection
    server.quit()

sender_email = "email@email.com"
sender_password = "password"
recipient_email = ["receptor1@hotmail.com", "receptor2@gmail.com"]
subject = "Asunto del correo"
body = "Este es el cuerpo del correo."

send_email(sender_email, sender_password, recipient_email, subject, body)