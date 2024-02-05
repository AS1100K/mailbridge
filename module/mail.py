import imaplib
import os
from module.custom_logging import log
from email.message import Message
from email import message_from_bytes
from email.utils import parsedate_to_datetime as p_dt
import pytz
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

            log.info("logging into Mail Server")
            self.mail.login(os.getenv(username), os.getenv(password))
        except Exception as e:
            log.error(f"`__init__` -> {e}")

    def get_number_of_emails(self, mailbox: str = "Inbox"):
        """
        :param mailbox: Mailbox i.e. 'Inbox', 'Drafts', etc.
        :return: int
        """
        try:
            log.debug(f"`get_number_of_emails`: mailbox -> {mailbox}")
            status, no_of_emails = self.mail.select(mailbox)
            self.mail.close()
            if status == 'OK':
                return no_of_emails
            else:
                raise Exception(f"`mail.uid` Status {status}")
        except Exception as e:
            log.error(f"`get_number_of_emails` -> {e}")
            return []

    def get_unread_messages(self, mailbox: str = "Inbox"):
        """
        :param mailbox: Mailbox i.e. 'Inbox', 'Drafts', etc.
        :return: list
        """
        try:
            log.debug(f"`get_unread_messages`: mailbox -> {mailbox}")
            self.mail.select(mailbox)
            status, uids = self.mail.uid('search', '(UNSEEN)')
            self.mail.close()
            if status == 'OK':
                return uids[0].decode('utf-8').split()
            else:
                raise Exception(f"mail.search Status {status}")
        except Exception as e:
            log.error(f"`get_unread_messages` -> {e}")
            return []

    # noinspection PyUnresolvedReferences
    def parse_email(self, uid: str, mailbox: str = "Inbox"):
        try:
            log.debug(f"Parsing Email UID -> {uid} mailbox -> {mailbox}")
            self.mail.select(mailbox)
            status, message = self.mail.uid('fetch', uid, 'RFC822')
            self.mail.close()
            if status == 'OK':
                new_message = message_from_bytes(message[0][1])
                return new_message
            else:
                raise Exception(message)
        except Exception as e:
            log.error(f"`parse_email -> {e}")
            return None

    def append_email(self, new_message: Message, mailbox: str = 'Inbox'):
        """
        Add the new_message to the specified mailbox.
        :param new_message: Message in the format of email.message.Message
        :param mailbox: Mailbox i.e. 'Inbox', 'Drafts', etc.
        :return: boolean
        """
        try:
            log.debug(f"`append_email` mailbox -> {mailbox} new_message['date'] -> {new_message['date']}")

            datetime_obj = p_dt(new_message['date'])
            # Check if the datetime is timezone aware
            if datetime_obj.tzinfo is None or datetime_obj.tzinfo.utcoffset(datetime_obj) is None:
                # If not timezone-aware, set the timezone to UTC
                datetime_obj = datetime_obj.replace(tzinfo=pytz.utc)

            log.info(f"Parsed Date Time -> {imaplib.Time2Internaldate(datetime_obj)}")
            self.mail.select(mailbox)
            encoded_message = str(new_message).encode('utf-8')
            status, msg = self.mail.append(mailbox, '', imaplib.Time2Internaldate(datetime_obj), encoded_message)
            self.mail.close()

            if status == 'OK':
                return True
            else:
                raise Exception(msg)
        except Exception as e:
            log.error(f"`append_email` -> {e}")
            return False

    def quit(self):
        self.mail.logout()
