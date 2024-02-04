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

    def get_latest_emails(self, mailbox: str = "INBOX"):
        """
        :return: list
        """
        categories = ["Social", "Updates", "Forums", "Promotional"]
        data = {
            "social": [],
            "updates": [],
            "forums": [],
            "promotional": []
        }
        try:
            self.mail.select(mailbox)
            for category in categories:
                status, response = self.mail.uid('search', 'X-GM-RAW "category:' + category + '"')

                # get email ids list
                response = response[0].decode('utf-8').split()
                response.reverse()
                data[category.lower()].append(response)
            return data
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
