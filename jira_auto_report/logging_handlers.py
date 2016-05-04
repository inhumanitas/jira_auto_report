# coding: utf-8

import logging

from jira_auto_report import settings
from jira_auto_report.notifiers import smpt_connection


class SMTPHandler(logging.Handler):
    """
    A handler class which sends an SMTP email for each logging event.
    """
    def __init__(self, subject=''):
        """
        Initialize the handler.

        Initialize the instance with the from and to addresses and subject
        line of the email. To specify a non-standard SMTP port, use the
        (host, port) tuple format for the mailhost argument. To specify
        authentication credentials, supply a (username, password) tuple
        for the credentials argument. To specify the use of a secure
        protocol (TLS), pass in a tuple for the secure argument. This will
        only be used when authentication credentials are supplied. The tuple
        will be either an empty tuple, or a single-value tuple with the name
        of a keyfile, or a 2-value tuple with the names of the keyfile and
        certificate file. (This tuple is passed to the `starttls` method).
        """
        logging.Handler.__init__(self)
        self.subject = subject
        self._timeout = 5.0

    def getSubject(self, record):
        """
        Determine the subject for the email.

        If you want to specify a subject line which is record-dependent,
        override this method.
        """
        return self.subject

    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            with smpt_connection(settings.mail_server_url,
                                 settings.user_mail,
                                 settings.user_password) as server:
                server.send_email(
                    settings.from_mail, settings.recipient, self.subject,
                    unicode(record))

        except (KeyboardInterrupt, SystemExit):
            raise

        except:
            self.handleError(record)
