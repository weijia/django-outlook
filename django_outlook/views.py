# from allauth.account.forms import LoginForm
# from allauth.socialaccount.providers.openid.forms import LoginForm
# from cms.test_utils.project.sampleapp.forms import LoginForm
# from allauth.account.forms import LoginForm
from django.views.generic import FormView, TemplateView, RedirectView

# from django_th.forms.base import LoginForm
from social.apps.django_app.default.models import AbstractUserSocialAuth, UserSocialAuth

# from django_outlook.forms import LoginForm

# class OutlookLoginFormView(FormView):
#     form_class = LoginForm
#     template_name = 'django_outlook/login_form.html'
#
#     def form_valid(self, form):
#         get_auth_url()
#         return super(OutlookLoginFormView, self).form_valid(form)
from django_outlook.o365_utils.connection import OutlookConnection
from djangoautoconf.django_utils import retrieve_param
from djangoautoconf.local_key_manager import get_local_key


class O365AuthRedirectView(RedirectView):
    permanent = False

    # query_string = True
    # pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        # article = get_object_or_404(Article, pk=kwargs['pk'])
        # article.update_counter()
        # return super().get_redirect_url(*args, **kwargs)
        c = OutlookConnection(get_local_key("o365_app_settings.o365_app_client_id"),
                                         get_local_key("o365_app_settings.o365_app_secret"))
        auth_url, state = c.get_auth_url()
        o, is_created = UserSocialAuth.objects.get_or_create(
            user=self.request.user,
            provider="o365",
            uid=self.request.user.username,
        )
        o.extra_data = {"state": state}
        o.save()
        return auth_url


class OutlookLoginResultView(TemplateView):
    template_name = 'django_outlook/key_got.html'

    def get_context_data(self, **kwargs):
        # return super(OutlookLoginResultView, self).get_context_data(**kwargs)
        # param = retrieve_param(self.request)
        c = OutlookConnection(get_local_key("o365_app_settings.o365_app_client_id"),
                                         get_local_key("o365_app_settings.o365_app_secret"))
        token_url = "%s/?%s" % ("https://localhost", self.request.META['QUERY_STRING'])
        social_auth = UserSocialAuth.objects.filter(
            user=self.request.user, provider="o365")[0]

        state = social_auth.extra_data["state"]
        try:
            token = c.update_token(token_url, state)
            o, is_created = UserSocialAuth.objects.get_or_create(
                user=self.request.user, provider="o365")
            o.extra_data = token
            o.save()
            res = {"json_key": str(token)}
        except Exception as e:
            res = {"json_key": str(e.message)}
        return res
