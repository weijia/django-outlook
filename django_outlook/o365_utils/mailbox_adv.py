from O365 import FluentInbox, Connection
from django_outlook.o365_utils.adv_connection import OutlookConnection


class AdvO365Mailbox(FluentInbox):
    adv_urls = {
        'auto_reply_setting': {
            '1.0': 'https://outlook.office365.com/api/v1.0/me/MailboxSettings/AutomaticRepliesSetting',
            '2.0': 'https://graph.microsoft.com/v1.0/me/MailboxSettings/AutomaticRepliesSetting',
        },
        'me': {
            '1.0': 'https://outlook.office365.com/api/v1.0/me',
            '2.0': 'https://graph.microsoft.com/v1.0/me',
        },
    }

    def get_auto_reply_setting(self):
        """
        :return: Current auto reply setting
        """
        auto_reply_setting_url = AdvO365Mailbox._get_url_v2('auto_reply_setting')

        response = OutlookConnection.get_common_response(auto_reply_setting_url,
                                                         # verify=self.verify,
                                                         # params={'$top': 100}
                                                         )

        return response

    @staticmethod
    def _get_url_v2(key):
        """ Fetches the url for specified key as per the connection version configured

        :param key: the key for which url is required
        :return: URL to use for requests
        """
        return AdvO365Mailbox.adv_urls[key][Connection().api_version]
