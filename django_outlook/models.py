from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields.json import JSONField
from django_extensions.db.models import TimeStampedModel
from social.apps.django_app.default.models import AbstractUserSocialAuth, UserSocialAuth


# class MicrosoftOauth(models.Model):
#     token_type = models.CharField(max_length=128)
#     refresh_token = models.TextField()
#     scope = models.TextField()
#     access_token = models.TextField()
#     expires_in = models.IntegerField()
#     ext_expires_in = models.IntegerField()
#     expires_at = models.FloatField()
#     user = models.ForeignKey(User)


class MailHandler(TimeStampedModel):
    auth = models.ForeignKey(UserSocialAuth)
    action = models.CharField(max_length=1024)
    parameters = JSONField(null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
