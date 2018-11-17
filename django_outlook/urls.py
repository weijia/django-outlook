from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

import models
from django_outlook.views import OutlookLoginResultView, O365AuthRedirectView
from djangoautoconf.model_utils.url_for_models import add_all_urls


urlpatterns = [
    url(r'result/', OutlookLoginResultView.as_view(), name="o365_token_update_view"),
    url(r'', O365AuthRedirectView.as_view(), name="o365_auth_redirect_view"),
    ]

add_all_urls(urlpatterns, models)
