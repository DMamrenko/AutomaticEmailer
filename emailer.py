import smtplib
from datetime import datetime
import os
import socket
from email.message import EmailMessage
import imghdr

class Emailer:
    def __init__(self, assignmentName):
        self.assignmentName = assignmentName
        self.EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        self.EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    def has_internet_connection(hostname):
        try:
            host = socket.gethostbyname(hostname)
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except:
            pass
        return False

    def send_email(self, recipient, subject, body, attachment):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.EMAIL_ADDRESS
        msg['To'] = recipient
        msg.set_content(body)
        attachment += '.png'
        with open(attachment, 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)

        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=attachment)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)
            smtp.send_message(msg)
