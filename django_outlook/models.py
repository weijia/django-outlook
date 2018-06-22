from django.contrib.auth.models import User
from django.db import models
from social.apps.django_app.default.models import AbstractUserSocialAuth, UserSocialAuth


class MicrosoftOauth(object):
    token_type = models.CharField(max_length=128)
    refresh_token = models.TextField()
    scope = models.TextField()
    access_token = models.TextField()
    expires_in = models.IntegerField()
    ext_expires_in = models.IntegerField()
    expires_at = models.FloatField()
    user = models.ForeignKey(User)
