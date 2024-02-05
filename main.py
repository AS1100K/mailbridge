from module.config import Config
from module.mail import Mail
from module.custom_logging import log
import time


def main():
    log.info("Loading Configuration file")
    config = Config("config/config.yml").configuration

    log.info("Connecting with Gmail - IMAP")
    gmail = Mail(username="G_EMAIL_USERNAME", password="G_PASSWORD", host_name="imap.gmail.com", host_port=993)

    log.info("Connecting with Outlook - IMAP")
    outlook = Mail()  # Default Configuration for Outlook.com

    # Return gmail or outlook as specified in `save_emails_in`
    mail = gmail if config['save_emails_in'] == "outlook" else outlook

    while True:
        if config['sync_unread_emails']:
            for i in range(len(config['sync_emails_folder'])):
                email_uids = mail.get_unread_messages(mailbox=config['sync_emails_folder'][i])
                for email_uid in email_uids:
                    # Break if string is empty
                    if email_uid == "":
                        break

                    message = mail.parse_email(email_uid, mailbox=config['sync_emails_folder'][i])
                    # Break is Parsing Failed
                    if message is None:
                        log.error("Email Message didn't parsed.")
                        break

                    # Save the email
                    transfer = outlook.append_email(message, mailbox=config['save_emails_folder'][i]) \
                        if config['save_emails_in'] == "outlook" \
                        else gmail.append_email(message, mailbox=config['save_emails_folder'][i])
                    if not transfer:
                        log.error(f"The email with uid {email_uid} did not went through")
                        break

                    # Delete the email
                    if config['delete_emails_after_transfer']:
                        mail.delete_email(email_uid, mailbox=config['sync_emails_folder'][i])
                        break
        else:
            log.error("`sync_unread_emails` == False is not supported till now. Post your issue on "
                      "https://github.com/adityajideveloper/mailbridge/issues")
            break

        time.sleep(1)  # Delay of 1 second in next iteration


if __name__ == "__main__":
    main()
