

class O365UrlGenerator(object):

    def __init__(self, target_mail):
        super(O365UrlGenerator, self).__init__()
        self.target_mail = target_mail

    def get_inbox_url(self):
        """
        Ref: https://stackoverflow.com/questions/40813610/microsoft-graph-api-net-not-able-to-read-shared-mail
        Ref: o365
        :return:
        """
        return 'https://graph.microsoft.com/v1.0/users/{user_id}/messages'.format(user_id=self.target_mail)

    def get_folders_url(self):
        return 'https://graph.microsoft.com/v1.0/users/{user_id}/MailFolders'.format(user_id=self.target_mail)
