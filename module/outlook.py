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

    def quit(self):
        self.mail.logout()
