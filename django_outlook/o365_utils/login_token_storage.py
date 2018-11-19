import string
from random import choice, randint

from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth

from django_outlook.o365_utils.token_storage import EmailForUserToAccessDoesNotExist


class LoginTokenStorage(object):
    """
    Store token in UserSocialAuth
    Need to keep the following info:
    1. user whose account is bind to this account
    2. user account (email) of this social auth
    3. service name
    4. role of this social auth

    uid: social account owner email
    provider: o365-outlook (if it is ongoing: o365-ongoing)
    user: current user
    """
    PROVIDER_FOR_ONGOING_AUTH = "o365-ongoing"
    PROVIDER = "o365-outlook"

    def __init__(self, current_user=None, mail_of_user_grant_the_token=None):
        super(LoginTokenStorage, self).__init__()
        self.mail_of_user_grant_the_token = mail_of_user_grant_the_token

    def get_token(self):
        auth = self._get_stored_social_auth()
        return auth.extra_data

    def save_first_token(self, token, user_info):
        characters = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(characters) for x in range(randint(8, 16)))
        user = self._get_user_from_email(user_info["mail"])
        user.password = password
        user.save()
        o, is_social_auth_created = UserSocialAuth.objects.get_or_create(
            user=user,
            provider=self.PROVIDER,
            uid=user_info["id"],
        )
        o.extra_data = token
        o.save()

    def save_token(self, token):
        o = self._get_stored_social_auth()
        o.extra_data = token
        o.save()

    def save_state(self, state):
        pass

    # noinspection PyMethodMayBeStatic
    def _get_user_from_email(self, user_email):
        user, is_user_created = User.objects.get_or_create(username=user_email,
                                                           email=user_email)
        return user

    def _get_stored_social_auth(self):
        if self.mail_of_user_grant_the_token is None:
            raise EmailForUserToAccessDoesNotExist
        user = self._get_user_from_email(self.mail_of_user_grant_the_token)
        auth = UserSocialAuth.objects.get(
            user=user,
            provider=self.PROVIDER,
        )
        return auth
