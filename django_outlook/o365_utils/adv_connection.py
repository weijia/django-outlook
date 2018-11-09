import logging
import os

from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session

from O365.connection import MicroDict
from djangoautoconf.local_key_manager import get_local_key

log = logging.getLogger(__name__)


# Ref: O365
class OutlookConnection(object):
    _oauth2_authorize_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    _oauth2_token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    api_version = '2.0'

    def __init__(self, client_id, client_secret, token_storage):
        super(OutlookConnection, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_id = self.client_id
        self.client_secret = self.client_secret
        self.token_storage = token_storage
        self.proxy_dict = None
        self.oauth = None
        # self.auth = None

        # Proxy call is required only if you are behind proxy
        self.set_proxy(url=get_local_key("proxy_setting.http_proxy_host"),
                       port=8080,
                       username=get_local_key("laptop_account.username"),
                       password=get_local_key("laptop_account.password")
                       )

    def set_proxy(self, url, port, username, password):
        """ Connect to Office 365 though the specified proxy

        :param url: url of the proxy server
        :param port: port to connect to proxy server
        :param username: username for authentication in the proxy server
        :param password: password for the specified username
        """

        self.proxy_dict = {
            "http": "http://{}:{}@{}:{}".format(username, password, url, port),
            "https": "https://{}:{}@{}:{}".format(username, password, url,
                                                  port),
        }

    def load_token(self):
        self.oauth = OAuth2Session(client_id=self.client_id,
                                         token=self.token_storage.get_token())

    def get_auth_url(self):
        self._set_oauth_session()
        auth_url, state = self.oauth.authorization_url(
            url=self._oauth2_authorize_url,
            access_type='offline')
        # username = user.username
        self.token_storage.save_state(state)
        return auth_url

    def update_extra_data(self, auth_resp):
        try:
            token = self._get_token(auth_resp, self.token_storage.get_stored_state())
            me_dict = self.get_me()
            self.token_storage.save_first_token(token, me_dict["mail"])
            res = {"json_key": str(token)}
        except Exception as e:
            res = {"json_key": str(e.message)}
        return res

    def _get_token(self, auth_resp, state):
        self._set_oauth_session(state)
        self.oauth.authorization_url(
            url=self._oauth2_authorize_url,
            access_type='offline')
        os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'Y'
        token = self.oauth.fetch_token(token_url=self._oauth2_token_url,
                                       authorization_response=auth_resp, client_secret=self.client_secret)

        return token

    def _set_oauth_session(self, state=None):
        self.oauth = OAuth2Session(client_id=self.client_id,
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

    def get_response(self, request_url, **kwargs):
        """ Fetches the response for specified url and arguments, adding the auth and proxy information to the url

        :param request_url: url to request
        :param kwargs: any keyword arguments to pass to the requests api
        :return: response object
        """
        response_json = self.get_common_response(request_url, **kwargs)

        if 'value' not in response_json:
            raise RuntimeError('Something went wrong, received an unexpected result \n{}'.format(response_json))

        response_values = [MicroDict(x) for x in response_json['value']]
        return response_values

    def get_common_response(self, request_url, **kwargs):
        con_params = {}
        if self.proxy_dict:
            con_params['proxies'] = self.proxy_dict
        con_params.update(kwargs)
        log.info('Requesting URL: {}'.format(request_url))
        try:
            response = self.oauth.get(request_url, **con_params)
        except TokenExpiredError:
            self.refresh_token()

            response = self.oauth.get(request_url, **con_params)
        log.info('Received response from URL {}'.format(response.url))
        response_json = response.json()
        return response_json

    def post_common_response(self, request_url, **kwargs):
        con_params = {}
        if self.proxy_dict:
            con_params['proxies'] = self.proxy_dict
        con_params.update(kwargs)
        log.info('Requesting URL: {}'.format(request_url))
        try:
            response = self.oauth.post(request_url, **con_params)
        except TokenExpiredError:
            self.refresh_token()

            response = self.oauth.post(request_url, **con_params)
        log.info('Received response from URL {}'.format(response.url))
        response_json = response.json()
        return response_json

    def refresh_token(self):
        log.info('Token is expired, fetching a new token')
        token = self.oauth.refresh_token(self._oauth2_token_url,
                                         client_id=self.client_id,
                                         client_secret=self.client_secret)
        log.info('New token fetched')
        self.token_storage.save_token(token)

    def get_me(self):
        """
        :return: Current auto reply setting
        """
        auto_reply_setting_url = 'https://graph.microsoft.com/v1.0/me'

        response = self.get_common_response(auto_reply_setting_url,
                                            # verify=self.verify,
                                            # params={'$top': 100}
                                            )

        return response
