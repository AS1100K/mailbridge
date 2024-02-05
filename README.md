# Mail Bridge
Mail Bridge is a simple Python program that let you choose what mailbox _(i.e. Outlook or Gmail)_ you want to use for storage of all your emails.

# Installation
1. Create a `compose.yml` file:
    ```yaml
    services:
      mailbridge:
        container_name: mailbridge
        image: adityaji/mailbridge
        volumes:
          - /path/to/your/config:/app/config
        environment:
          O_EMAIL_USERNAME: "username@outlook.com"
          O_PASSWORD: "your_very_secure_outlook_password"
          G_EMAIL_USERNAME: "username@gmail.com"
          G_PASSWORD: "your_very_secure_gmail_password"
    ```
2. Create `config/config.yml`:
    ```yaml
    save_emails_in: outlook
    delete_emails_after_transfer: true
    sync_unread_emails: true
    sync_emails_folder:
      - Inbox
      - Draft
      - All Mail
    save_emails_folder:
      - Inbox
      - Inbox.Draft
      - Archive
    ```
3. Run the container
    ```bash
   docker compose up -d
    ```

# Configuring you own `config.yml`
| Parameter                    | Use case                                                   | Values               | Required |
|------------------------------|------------------------------------------------------------|----------------------|----------|
| save_emails_in               | Mailbox you want to save all your new emails in            | `outlook` or `gmail` | `True`   |
| delete_emails_after_transfer | Delete the emails after tranfering into your other mailbox | `true` or `false`    | `True`   |
| sync_unread_emails           | To transfer only unread emails                             | `true`               | `True`   |
| sync_emails_folder           | Email folder from which emails will be transferred         | `Array`              | `True`   |
| save_emails_folder           | Email folder to which emails will be transferred           | `Array`              | `True`   |

_**NOTE: `sync_emails_folder` and `save_emails_folder` must be in same order from top to bottom as you intend them to work.**_