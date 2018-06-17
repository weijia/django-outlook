# coding=utf-8
from O365 import Connection, FluentInbox
from O365.fluent_message import Message
from django_outlook.management.o365mail import O365Mail
from django_outlook.management.outlook_mail import OutlookMail

from djangoautoconf.local_key_manager import get_local_key


class O365Base(object):
    def __init__(self):
        """
        :param mailbox_name_pattern: not used. This is kept only for be compatible with the pywin implementation
        """
        # Setup connection object
        # Proxy call is required only if you are behind proxy

        # Setup connection object
        # This will provide you with auth url, open it and authentication and copy the resulting page url and
        # paste it back in the input
        o365_app_client_id = get_local_key("o365_app_settings.o365_app_client_id")
        o365_app_secret = get_local_key("o365_app_settings.o365_app_secret")
        Connection.oauth2(o365_app_client_id, o365_app_secret, store_token=True)

        # Proxy call is required only if you are behind proxy
        Connection.proxy(url='10.138.15.11',
                         port=8080,
                         username=get_local_key("laptop_account.username"),
                         password=get_local_key("laptop_account.password")
                         )
        self.fluent_inbox = FluentInbox()


class OutlookReaderForO365(O365Base):
    def __init__(self, mailbox_name_pattern=None):
        """
        :param mailbox_name_pattern: not used, this parameter is only kept for be compatible with pywin32 implementation
        """
        super(OutlookReaderForO365, self).__init__()

    # def get_inbox(self):
    #     inbox = self.get_mailbox_folder(u'Inbox')
    #     if inbox is None:
    #         inbox = self.get_mailbox_folder(u"收件箱")
    #     return inbox
    #
    # def get_mailbox_folder(self, folder_name):
    #     return self.fluent_inbox.get_folder(by='DisplayName', value=folder_name)

    def enum_inbox_mails(self, count=1000):
        mail = self.fluent_inbox.fetch(1)[0]
        yield O365Mail(mail)
        for i in xrange(1, count):
            mail = self.fluent_inbox.fetch_next()[0]
            yield O365Mail(mail)

    def get_folder(self, mailbox_name_pattern):
        fluent_inbox = FluentInbox().get_folder(by='DisplayName', value=mailbox_name_pattern)
        return fluent_inbox

    def move_mail(self, outlook_mail, target_folder):
        outlook_mail.raw_mail.moveToFolder(target_folder["id"])
