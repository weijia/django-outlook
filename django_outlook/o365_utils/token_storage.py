from social.apps.django_app.me.models import UserSocialAuth


class EmailForUserToAccessDoesNotExist(Exception):
    pass


class TokenStorage(object):
    """
    Store token in UserSocialAuth
    Need to keep the following info:
    1. user whose account is bind to this account
    2. user account (email) of this social auth
    3. service name
    4. role of this social auth

    uid: social account owner email
    provider: o365 (if it is ongoing: o365-ongoing)
    user: current user
    """
    PROVIDER_FOR_ONGOING_AUTH = "o365-ongoing"
    PROVIDER = "o365"

    def __init__(self, current_user, user_to_access_using_the_token=None):
        super(TokenStorage, self).__init__()
        self.current_user = current_user
        self.user_to_access_using_the_token = user_to_access_using_the_token

    def save_token(self, token):
        if self.user_to_access_using_the_token is None:
            raise EmailForUserToAccessDoesNotExist
        o = self._get_ongoing_social_auth(self.user_to_access_using_the_token)
        o.extra_data = token
        o.uid = self.user_to_access_using_the_token.email
        o.provider = self.PROVIDER
        o.save()

    def _get_ongoing_social_auth(self):
        return UserSocialAuth.objects.get(
            user=self.current_user,
            provider=self.PROVIDER_FOR_ONGOING_AUTH,
            uid=self.current_user.username
        )

    def save_state(self, state):
        o, is_created = UserSocialAuth.objects.get_or_create(
            user=self.user_to_access_using_the_token,
            provider=self.PROVIDER_FOR_ONGOING_AUTH,
            uid=self.user_to_access_using_the_token.username,
        )
        o.extra_data = {"state": state}
        o.save()
