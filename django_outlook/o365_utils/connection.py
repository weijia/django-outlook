import os
from requests_oauthlib import OAuth2Session
from O365 import Connection
from djangoautoconf.local_key_manager import get_local_key


class OutlookConnection(object):
    def __init__(self, client_id, client_secret):
        super(OutlookConnection, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.connection = Connection()
        self.connection.api_version = '2.0'
        self.connection.client_id = self.client_id
        self.connection.client_secret = self.client_secret

        # Proxy call is required only if you are behind proxy
        Connection.proxy(url=get_local_key("proxy_setting.http_proxy_host"),
                         port=8080,
                         username=get_local_key("laptop_account.username"),
                         password=get_local_key("laptop_account.password")
                         )

    def get_auth_url(self):
        self._set_oauth_session()
        oauth = self.connection.oauth
        auth_url, state = oauth.authorization_url(
            url=Connection._oauth2_authorize_url,
            access_type='offline')
        return auth_url, state

    def update_token(self, auth_resp, state):
        self._set_oauth_session(state)
        auth_url, state = self.connection.oauth.authorization_url(
            url=Connection._oauth2_authorize_url,
            access_type='offline')
        os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'Y'
        token = self.connection.oauth.fetch_token(token_url=Connection._oauth2_token_url,
                                                  authorization_response=auth_resp, client_secret=self.client_secret)

        return token

    def _set_oauth_session(self, state=None):
        self.connection.oauth = OAuth2Session(client_id=self.client_id,
                                              redirect_uri='https://outlook.office365.com/owa/',
                                              scope=[
                                                  'https://graph.microsoft.com/Mail.ReadWrite',
                                                  'https://graph.microsoft.com/Mail.Send',
                                                  'https://graph.microsoft.com/User.Read',
                                                  # 'https://outlook.office.com/mail.readwrite',
                                                  'offline_access',
                                                  'https://graph.microsoft.com/mailboxsettings.readwrite'
                                              ],
                                              state=state
                                              )

    def set_token(self, token):
        self.connection.oauth = OAuth2Session(
            client_id=self.client_id,
            token=token
        )
