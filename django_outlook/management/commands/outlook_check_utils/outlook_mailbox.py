# coding=utf-8
import win32com

from django_outlook.management.outlook_mail import OutlookMail
from djangoautoconf.local_key_manager import get_local_key


class OutlookMailboxBase(object):
    def __init__(self, mailbox_name_pattern=None):
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.__mailbox_name_pattern = mailbox_name_pattern
        self.inbox = None
        self.mailbox_items = None

    def get_folder(self, folder_name):
        mailbox = self.__get_mailbox()
        return self.__get_folder_in_mailbox(mailbox, folder_name)

    def __get_mailbox(self):
        """
        Get the mailbox from outlook. Folder are below mailbox
        :param mailbox_name: The name of the mailbox, normally it is xxxx.x.x@xxx.com
        :return: the mailbox for the name
        """
        # target_folder_index = None
        if self.__mailbox_name_pattern is None:
            self.__mailbox_name_pattern = get_local_key("outlook_settings.mailbox_name_pattern")

        for mailbox_number in range(1, 100):
            # Admin
            print unicode(self.outlook.Folders.Item(mailbox_number).Name).encode("gbk", "replace")
            if self.__mailbox_name_pattern in self.outlook.Folders.Item(mailbox_number).Name:
                # print mailbox_number
                return self.outlook.Folders.Item(mailbox_number)

    # noinspection PyMethodMayBeStatic
    def __get_folder_in_mailbox(self, mailbox, folder_name):
        for folder_number in range(1, 100):
            try:
                folder = mailbox.Folders.Item(folder_number)
            except:
                return None
            if folder_name in folder.Name:
                return folder

    def enum_inbox_mails(self, count=1000):
        self.inbox = self.get_inbox()
        self.mailbox_items = self.inbox.Items
        mail = self.get_last_mail()
        yield OutlookMail(mail)
        for cnt in range(1, count):
            yield OutlookMail(mail)
            mail = self.get_previous_email()

    def get_last_mail(self):
        self.mailbox_items.Sort("[ReceivedTime]")
        return self.mailbox_items.GetLast()

    def get_previous_email(self):
        self.mailbox_items.Sort("[ReceivedTime]")
        previous_email = self.mailbox_items.GetPrevious()
        if previous_email is not None:
            return previous_email
        else:
            return None


class OutlookMailbox(OutlookMailboxBase):
    def get_inbox(self):
        inbox = self.get_folder("Inbox")
        if inbox is None:
            inbox = self.get_folder(u"收件箱")
        return inbox

    # def move_mail(self, outlook_mail, resolved_items_folder):
    #     outlook_mail.move(resolved_items_folder)