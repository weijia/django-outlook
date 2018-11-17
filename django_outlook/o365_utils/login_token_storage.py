import string
from random import choice, randint

from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth


class EmailForUserToAccessDoesNotExist(Exception):
    pass


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

    def __init__(self, current_user, mail_of_user_grant_the_token=None):
        super(LoginTokenStorage, self).__init__()
        self.current_user = current_user
        self.mail_of_user_grant_the_token = mail_of_user_grant_the_token

    def get_token(self):
        if self.mail_of_user_grant_the_token is None:
            raise EmailForUserToAccessDoesNotExist
        auth = self.get_auth_obj()
        return auth.extra_data

    def save_first_token(self, token, user_info):
        characters = string.ascii_letters + string.punctuation + string.digits
        password = "".join(choice(characters) for x in range(randint(8, 16)))
        user, is_user_created = User.objects.get_or_create(username=user_info["mail"],
                                                           email=user_info["mail"], )
        user.password = password
        o, is_social_auth_created = UserSocialAuth.objects.get_or_create(
            user=user,
            provider=self.PROVIDER,
            uid=user_info["id"],
        )
        o.extra_data = token
        o.save()

    def get_stored_social_auth(self, uid):
        return UserSocialAuth.objects.get(
            user=self.current_user,
            provider=self.PROVIDER,
            uid=uid,
        )

    def save_token(self, token):
        pass

    def get_auth_obj(self):
        return self.get_stored_social_auth(self.get_uid())

    def _get_ongoing_social_auth(self):
        return UserSocialAuth.objects.get(
            user=self.current_user,
            provider=self.PROVIDER_FOR_ONGOING_AUTH,
            uid=self.get_uid(),
        )

    def get_stored_state(self):
        social_auth = self._get_ongoing_social_auth()
        state = social_auth.extra_data["state"]
        return state

    def save_state(self, state):
        pass

    def get_uid(self):
        if self.mail_of_user_grant_the_token is None:
            uid = "unknown"
        else:
            uid = self.mail_of_user_grant_the_token
        return uid

    def set_mail_of_user_grant_the_token(self, mail):
        self.mail_of_user_grant_the_token = mail

    def is_stored_social_auth_exists(self, uid):
        return UserSocialAuth.objects.filter(
            user=self.current_user,
            provider=self.PROVIDER,
            uid=uid,
        ).exists()
