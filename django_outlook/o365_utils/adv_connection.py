import logging
import os

import requests
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
from social.apps.django_app.default.models import UserSocialAuth

from O365 import Connection
from django_outlook.o365_utils.mailbox_adv import AdvO365Mailbox
from djangoautoconf.local_key_manager import get_local_key


from O365.connection import MicroDict


log = logging.getLogger(__name__)


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

    def get_auth_url(self, user):
        self._set_oauth_session()
        oauth = self.connection.oauth
        auth_url, state = oauth.authorization_url(
            url=Connection._oauth2_authorize_url,
            access_type='offline')
        username = user.username
        o, is_created = UserSocialAuth.objects.get_or_create(
            user=user,
            provider="o365-ongoing",
            uid=username,
        )
        o.extra_data = {"state": state}
        o.save()

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

    def update_extra_data(self, user, token_url):
        social_auth = self._get_ongoing_social_auth(user)
        state = social_auth.extra_data["state"]
        try:
            token = self.update_token(token_url, state)
            o = self._get_ongoing_social_auth(user)
            o.extra_data = token
            me = AdvO365Mailbox().get_me()
            o.uid = me["mail"]
            o.provider = "o365"
            o.save()
            res = {"json_key": str(token)}
        except Exception as e:
            res = {"json_key": str(e.message)}
        return res

    @staticmethod
    def _get_ongoing_social_auth(user):
        return UserSocialAuth.objects.get(
            user=user,
            provider="o365-ongoing",
            uid=user.username
        )

    @staticmethod
    def get_response(request_url, **kwargs):
        """ Fetches the response for specified url and arguments, adding the auth and proxy information to the url

        :param request_url: url to request
        :param kwargs: any keyword arguments to pass to the requests api
        :return: response object
        """
        response_json = OutlookConnection.get_common_response(request_url, **kwargs)

        if 'value' not in response_json:
            raise RuntimeError('Something went wrong, received an unexpected result \n{}'.format(response_json))

        response_values = [MicroDict(x) for x in response_json['value']]
        return response_values

    @staticmethod
    def get_common_response(request_url, **kwargs):
        connection = Connection()
        if not connection.is_valid():
            raise RuntimeError('Connection is not configured, please use "O365.Connection" '
                               'to set username and password or OAuth2 authentication')
        con_params = {}
        if connection.proxy_dict:
            con_params['proxies'] = connection.proxy_dict
        con_params.update(kwargs)
        log.info('Requesting URL: {}'.format(request_url))
        if connection.api_version == '1.0':
            con_params['auth'] = connection.auth
            response = requests.get(request_url, **con_params)
        else:
            try:
                response = connection.oauth.get(request_url, **con_params)
            except TokenExpiredError:
                log.info('Token is expired, fetching a new token')
                token = connection.oauth.refresh_token(Connection._oauth2_token_url, client_id=connection.client_id,
                                                       client_secret=connection.client_secret)
                log.info('New token fetched')
                save_token(token)

                response = connection.oauth.get(request_url, **con_params)
        log.info('Received response from URL {}'.format(response.url))
        response_json = response.json()
        return response_json
