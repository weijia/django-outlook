import win32com

from djangoautoconf.local_key_manager import get_local_key


class OutlookReader(object):
    def __init__(self, mailbox_name_pattern=None):
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.mailbox_name_pattern = mailbox_name_pattern

    def get_inbox(self):
        if self.mailbox_name_pattern is None:
            self.mailbox_name_pattern = get_local_key("outlook_settings.mailbox_name_pattern")
        return self.get_mailbox_folder(self.mailbox_name_pattern, "Inbox")

    def get_mailbox_folder(self, mailbox_pattern, folder_name):
        mailbox = self.get_mailbox(mailbox_pattern, self.outlook)
        return self.get_folder_in_mailbox(mailbox, folder_name)

    def get_mailbox(self, mailbox_name, outlook):
        # target_folder_index = None
        for mailbox_number in range(1, 100):
            # Admin
            print unicode(outlook.Folders.Item(mailbox_number).Name).encode("gbk", "replace")
            if mailbox_name in self.outlook.Folders.Item(mailbox_number).Name:
                # print mailbox_number
                return self.outlook.Folders.Item(mailbox_number)

    # noinspection PyMethodMayBeStatic
    def get_folder_in_mailbox(self, mailbox, folder_name):
        for folder_number in range(1, 100):
            if folder_name in mailbox.Folders.Item(folder_number).Name:
                return mailbox.Folders.Item(folder_number)

