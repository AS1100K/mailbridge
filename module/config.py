from yaml import safe_load
from os import path
import logging


class Config:
    def __init__(self, file_location: str):
        try:
            if path.exists(file_location):
                with open(file_location, 'r') as file:
                    self.configuration = safe_load(file)
                    if len(self.configuration['sync_emails_folder']) != len(self.configuration['save_emails_folder']):
                        raise Exception("`sync_email_folder` and `save_email_folder` length doesn't match.")
                    if type(self.configuration['save_emails_in']) != str:
                        raise Exception("`save_emails_in` must be a string")
                    if type(self.configuration['delete_email_after_transfer']) != bool:
                        raise Exception("`delete_email_after_transfer` must be a bool")
                    if type(self.configuration['sync_unread_emails']) != bool:
                        raise Exception("`sync_unread_emails` must be a bool")
            else:
                raise Exception("Config File doesn't exists")
        except Exception as e:
            logging.error(e)
