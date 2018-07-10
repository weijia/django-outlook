from O365 import Connection, FluentInbox
from django_outlook.management.o365mail import O365Mail
from django_outlook.o365_utils.connection import OutlookConnection
from django_outlook.o365_utils.mailbox_adv import AdvO365Mailbox

from djangoautoconf.local_key_manager import get_local_key


def config_connection_using_config_template():
    # Setup connection object
    # Proxy call is required only if you are behind proxy

    # Setup connection object
    # This will provide you with auth url, open it and authentication and copy the resulting page url and
    # paste it back in the input
    o365_app_client_id = get_local_key("o365_app_settings.o365_app_client_id")
    o365_app_secret = get_local_key("o365_app_settings.o365_app_secret")
    Connection.oauth2(o365_app_client_id, o365_app_secret, store_token=True)

    # Proxy call is required only if you are behind proxy
    Connection.proxy(url=get_local_key("proxy_setting.http_proxy_host"),
                     port=8080,
                     username=get_local_key("laptop_account.username"),
                     password=get_local_key("laptop_account.password")
                     )


class OutlookReaderForO365(object):
    def __init__(self, mailbox_name_pattern=None, token=None):
        """
        :param mailbox_name_pattern: not used, this parameter is only kept for be compatible with pywin32 implementation
        """
        super(OutlookReaderForO365, self).__init__()
        if token is None:
            config_connection_using_config_template()
        else:
            o365_app_client_id = get_local_key("o365_app_settings.o365_app_client_id")
            o365_app_secret = get_local_key("o365_app_settings.o365_app_secret")
            self.connection = OutlookConnection(client_id=o365_app_client_id, client_secret=o365_app_secret)
            self.connection.set_token(token)

        self.fluent_inbox = FluentInbox()
        self.adv_mailbox = AdvO365Mailbox()

    def enum_inbox_mails(self, count=1000):
        text = self.adv_mailbox.get_me()
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
