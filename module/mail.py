import imaplib
import os
import logging
from email.message import Message
from email import message_from_bytes, utils
from dotenv import load_dotenv

load_dotenv()


class Mail:
    def __init__(self, username: str = "O_EMAIL_USERNAME", password: str = "O_PASSWORD",
                 host_name: str = "outlook.office365.com", host_port: int = 993):
        """
        Connect with the IMAP server. Default Configured for Outlook.
        :param username: ENV Variable Name
        :param password: ENV Variable Name
        :param host_name: IMAP host url
        :param host_port: IMAP host port
        """
        try:
            self.mail = imaplib.IMAP4_SSL(host_name, port=host_port)
            # context = ssl.create_default_context()
            # self.mail.starttls(ssl_context=context)

            logging.info("Logging in Outlook Mail Server")
            self.mail.login(os.getenv(username), os.getenv(password))
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
                return no_of_emails
            else:
                raise Exception(f"`mail.uid` Status {status}")
        except Exception as e:
            logging.error(e)
            return []

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
            return []

    # noinspection PyUnresolvedReferences
    def parse_email(self, uid: str, mailbox: str = "Inbox"):
        try:
            self.mail.select(mailbox)
            status, message = self.mail.fetch(uid, 'RFC822')
            if status == 'OK':
                new_message = message_from_bytes(message[0][1])
                return new_message
            else:
                raise Exception(message)
        except Exception as e:
            logging.error(e)
            return None

    def append_email(self, new_message: Message, mailbox: str = 'Inbox'):
        """
        Add the new_message to the specified mailbox.
        :param new_message: Message in the format of email.message.Message
        :param mailbox: Mailbox i.e. 'Inbox', 'Drafts', etc.
        :return: boolean
        """
        try:
            self.mail.select(mailbox)
            encoded_message = str(new_message).encode('utf-8')
            status, msg = self.mail.append(mailbox, '', imaplib.Time2Internaldate(utils.parsedate_to_datetime(new_message['date'])), encoded_message)

            if status == 'OK':
                return True
            else:
                raise Exception(msg)
        except Exception as e:
            logging.error(e)
            return None

    def delete_email(self, uid: str, mailbox: str = 'Inbox'):
        """
        Delete a specific email from the mailbox
        """
        try:
            self.mail.select(mailbox)
            self.mail.store(uid, '+FLAGS', '\\Deleted')
        except Exception as e:
            logging.error(e)
            return None

    def quit(self):
        self.mail.logout()
