import imaplib
import os
import logging

from dotenv import load_dotenv

load_dotenv()


class Outlook:
    def __init__(self, host_name: str = "outlook.office365.com", host_port: int = 993):
        try:
            self.mail = imaplib.IMAP4_SSL(host_name, port=host_port)
            # context = ssl.create_default_context()
            # self.mail.starttls(ssl_context=context)

            logging.info("Logging in Outlook Mail Server")
            self.mail.login(os.getenv("O_EMAIL_USERNAME"), os.getenv("O_PASSWORD"))
        except Exception as e:
            logging.error(e)

    def get_number_of_emails(self, mailbox: str = "Inbox"):
        """
        :param mailbox: Mailbox i.e. 'Inbox', 'Drafts', etc.
        :return: int
        """
        try:
            status, no_of_emails = self.mail.select(mailbox)
            if status == 'OK':
                return no_of_emails.decode('utf-8')
            else:
                raise Exception(f"`mail.uid` Status {status}")
        except Exception as e:
            logging.error(e)
            return None

    def get_unread_messages(self, mailbox: str = "Inbox"):
        """
        :param mailbox: Mailbox i.e. 'Inbox', 'Drafts', etc.
        :return: list
        """
        try:
            self.mail.select(mailbox)
            status, uids = self.mail.search(None, '(UNSEEN)')
            if status == 'OK':
                return uids
            else:
                raise Exception(f"mail.search Status {status}")
        except Exception as e:
            logging.error(e)
            return None

    def quit(self):
        self.mail.logout()
