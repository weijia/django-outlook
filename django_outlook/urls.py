from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

import models
from django_outlook.views import OutlookLoginResultView, O365AuthRedirectView, O365LoginRedirectView, \
    OutlookAuthResultView
from djangoautoconf.model_utils.url_for_models import add_all_urls


urlpatterns = [
    url(r'login_result/', OutlookLoginResultView.as_view(), name="o365_login_view"),
    url(r'login/', O365LoginRedirectView.as_view(), name="o365_login_redirect_view"),
    url(r'result/', login_required(OutlookAuthResultView.as_view()), name="o365_token_update_view"),
    url(r'', login_required(O365AuthRedirectView.as_view()), name="o365_auth_redirect_view"),
    ]

add_all_urls(urlpatterns, models)
