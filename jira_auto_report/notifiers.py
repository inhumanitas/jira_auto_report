# coding: utf-8

from __future__ import unicode_literals

import smtplib
import socket
import logging
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class SMTPServerUnavailable(Exception):
    pass


class smpt_connection(object):
    def __init__(self, server_url, user_mail=None, password=None):
        super(smpt_connection, self).__init__()

        self.server_url = server_url
        self.user_name = user_mail
        self.password = password

    def __enter__(self):
        try:
            server = smtplib.SMTP(self.server_url)
        except socket.error as err:
            logger.critical(err)
            raise SMTPServerUnavailable()

        if self.user_name and self.password:
            server.ehlo()
            server.starttls()
            server.login(self.user_name, self.password)

        self.server = server

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.close()

    def send_email(self, user_from, recipient, subject, message):
        users_to = recipient if type(recipient) is list else [recipient]

        mime_message = MIMEText(message.encode('utf-8'), _charset='utf-8')
        mime_message['Subject'] = subject
        mime_message['From'] = user_from

        try:
            self.server.sendmail(user_from, users_to, mime_message.as_string())
        except:
            raise

        logger.info(message)


def get_local_server():
    try:
        server = smtplib.SMTP("localhost", 1025)
    except socket.error:
        return None

    return server
