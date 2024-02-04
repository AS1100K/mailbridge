from module.config import Config
from module.mail import Mail
import logging


def main():
    logging.info("Loading Configuration file")
    config = Config("config.yml").configuration

    logging.info("Connecting with Gmail - IMAP")
    gmail = Mail(username="G_EMAIL_USERNAME", password="G_PASSWORD", host_name="imap.gmail.com", host_port=993)

    logging.info("Connecting with Outlook - IMAP")
    outlook = Mail() # Default Configuration for Outlook.com

    # Looping through data continuously
    print(config)
    while True:
        if config['sync_unread_emails']:
            unread_emails = gmail.get_unread_messages() if config['save_emails_in'] == "outlook" else outlook.get_unread_messages()

            if len(unread_emails) >= 1:
                for unread_email in unread_emails:
                    uid = unread_email.decode('utf-8')
                    email = gmail.parse_email(uid) if config['save_emails_in'] == "outlook" else outlook.parse_email(
                        uid)
                    outlook.append_email(email) if config['save_emails_in'] == "outlook" else gmail.append_email(email)

                    # Delete Emails
                    if config['delete_emails_after_transfer']:
                        gmail.delete_email(uid) if config['save_emails_in'] == "outlook" else outlook.delete_email(uid)

        # Deleting Emails Permanently
        if config['delete_emails_after_transfer']:
            gmail.mail.expunge() if config['save_emails_in'] == "outlook" else outlook.mail.expunge()


if __name__ == "__main__":
    main()
