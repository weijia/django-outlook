import os

from requests_oauthlib import OAuth2Session

from O365 import Connection


class OutlookConnection(Connection):

    def __init__(self):
        super(OutlookConnection, self).__init__()
        self.connection = None

    def get_auth_url(self, client_id, client_secret):
        self.connection = Connection()
        self.connection.api_version = '2.0'
        self.connection.client_id = client_id
        self.connection.client_secret = client_secret

        self.connection.oauth = OAuth2Session(client_id=client_id,
                                              redirect_uri='https://outlook.office365.com/owa/',
                                              scope=['https://graph.microsoft.com/Mail.ReadWrite',
                                                     'https://graph.microsoft.com/Mail.Send',
                                                     # 'https://outlook.office.com/mail.readwrite',
                                                     'offline_access',
                                                     'https://graph.microsoft.com/mailboxsettings.readwrite'])
        oauth = self.connection.oauth
        auth_url, state = oauth.authorization_url(
            url=Connection._oauth2_authorize_url,
            access_type='offline')
        return auth_url, state

    def update_token(self, client_id, client_secret, auth_resp, state):
        connection = Connection()

        connection.api_version = '2.0'
        connection.client_id = client_id
        connection.client_secret = client_secret

        connection.oauth = OAuth2Session(client_id=client_id,
                                         redirect_uri='https://outlook.office365.com/owa/',
                                         scope=[
                                             'https://graph.microsoft.com/Mail.ReadWrite',
                                             # 'https://graph.microsoft.com/Mail.Send',
                                             # 'https://outlook.office.com/mail.readwrite',
                                             # 'offline_access',
                                             # 'https://graph.microsoft.com/mailboxsettings.readwrite'
                                         ],
                                         state=state
                                         )
        oauth = connection.oauth
        auth_url, state = oauth.authorization_url(
            url=Connection._oauth2_authorize_url,
            access_type='offline')
        # print('Please open {} and authorize the application'.format(auth_url))
        # auth_resp = raw_input('Enter the full result url: ')
        # auth_resp = auth_resp.strip()
        os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'Y'
        token = oauth.fetch_token(token_url=Connection._oauth2_token_url,
                                  authorization_response=auth_resp, client_secret=client_secret)

        return token
