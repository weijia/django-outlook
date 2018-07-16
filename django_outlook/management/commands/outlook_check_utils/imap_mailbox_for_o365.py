from O365 import FluentInbox
from django_outlook.management.o365mail import O365Mail
from django_outlook.o365_utils.adv_connection import OutlookConnection
from django_outlook.o365_utils.fluent_inbox_adv import FluentInboxAdv
from djangoautoconf.local_key_manager import get_local_key


class OutlookReaderForO365(object):
    def __init__(self, mailbox_name_pattern=None, token_storage=None):
        """
        :param mailbox_name_pattern: not used, this parameter is only kept for be compatible with pywin32 implementation
        """
        super(OutlookReaderForO365, self).__init__()
        o365_app_client_id = get_local_key("o365_app_settings.o365_app_client_id")
        o365_app_secret = get_local_key("o365_app_settings.o365_app_secret")

        self.connection = OutlookConnection(client_id=o365_app_client_id,
                                            client_secret=o365_app_secret,
                                            token_storage=token_storage,
                                            )
        self.connection.load_token()
        self.fluent_inbox = FluentInboxAdv(connection=self.connection)

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
        outlook_mail.raw_mail.moveToFolder(str(target_folder["id"]))
