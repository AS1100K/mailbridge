import imaplib
import email
import os
import logging

from dotenv import load_dotenv

load_dotenv()


class Gmail:
    def __init__(self, host_name: str = "imap.gmail.com", host_port: int = 993):
        try:
            self.mail = imaplib.IMAP4_SSL(host_name, port=host_port)
            self.mail.login(os.getenv('G_EMAIL_USERNAME'), os.getenv('G_PASSWORD'))
        except Exception as e:
            logging.error(e)

    def list_mailbox(self):
        code, mailboxes = self.mail.list()
        response = []
        for mailbox in mailboxes:
            mailbox = mailbox.decode('utf-8')
            mailbox = mailbox.split(") ")[1]
            mailbox = mailbox.split(' "')[1]
            mailbox = mailbox.split('"')[0]
            response.append(mailbox)

        return response

    def get_no_of_emails(self, mailbox: str = "INBOX"):
        """
        :param mailbox: Mailbox i.e. 'Inbox', [GMAIL]/All Mail', etc.
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

    def get_unread_messages(self, mailbox: str = "INBOX"):
        """
        :param mailbox: Mailbox i.e. 'Inbox', [GMAIL]/All Mail', etc.
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

    def get_email_content(self, uid: int, mailbox: str = "INBOX"):
        """
        :param uid: UID of the mail to view content
        :param mailbox: Mailbox i.e. 'Inbox', '[GMAIL]/All Mail', etc. Use list_mailbox() for view all
        :return:
        """
        self.mail.select(mailbox)
        status, data = self.mail.uid('fetch', str(uid), '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                return email.message_from_bytes(response_part[1])

    def quit(self):
        self.mail.logout()