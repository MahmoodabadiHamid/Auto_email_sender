import pandas as pd
import smtplib
from email.message import EmailMessage
import mimetypes

class EmailSender:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        
    def send_email(self, to_email, subject, body, attachment_path=None):
        try:
            # Create an email message object
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = to_email
            #msg['Bcc'] = self.sender_email  
            # Add an attachment if provided
            if attachment_path:
                mime_type, _ = mimetypes.guess_type(attachment_path)
                if mime_type is None:
                    mime_type = 'application/octet-stream'
                mime_type, mime_subtype = mime_type.split('/', 1)
                # Open the file in binary mode and attach it
                with open(attachment_path, 'rb') as file:
                    msg.add_attachment(file.read(),
                                       maintype=mime_type,
                                       subtype=mime_subtype,
                                       filename=attachment_path.split('/')[-1])

            # Connect to SMTP server and send the message
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            print(f"Email sent to {to_email}")

        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")


