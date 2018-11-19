from django.views.generic import TemplateView, RedirectView
from django_outlook.o365_utils.adv_connection import OutlookConnection
from django_outlook.o365_utils.login_token_storage import LoginTokenStorage
from django_outlook.o365_utils.token_storage import TokenStorage
from djangoautoconf.django_utils import retrieve_param
from djangoautoconf.local_key_manager import get_local_key


class O365AuthRedirectView(RedirectView):
    permanent = False  # Not always redirect to the same page

    def get_redirect_url(self, *args, **kwargs):
        # article = get_object_or_404(Article, pk=kwargs['pk'])
        # article.update_counter()
        # return super().get_redirect_url(*args, **kwargs)
        token_storage = TokenStorage(self.request.user)
        c = OutlookConnection(
            get_local_key("o365_app_settings.o365_app_client_id"),
            get_local_key("o365_app_settings.o365_app_secret"),
            token_storage,
        )
        auth_url = c.get_auth_url()
        return auth_url


class OutlookAuthResultView(TemplateView):
    template_name = 'django_outlook/key_got.html'

    def get_context_data(self, **kwargs):
        # return super(OutlookAuthResultView, self).get_context_data(**kwargs)
        # param = retrieve_param(self.request)
        token_storage = TokenStorage(self.request.user)
        c = OutlookConnection(
            get_local_key("o365_app_settings.o365_app_client_id"),
            get_local_key("o365_app_settings.o365_app_secret"),
            token_storage,
        )
        token_url = "%s/?%s" % ("https://localhost", self.request.META['QUERY_STRING'])

        res = c.update_extra_data(token_url)
        return res


class O365LoginRedirectView(RedirectView):
    permanent = False  # Not always redirect to the same page

    def get_redirect_url(self, *args, **kwargs):
        # article = get_object_or_404(Article, pk=kwargs['pk'])
        # article.update_counter()
        # return super().get_redirect_url(*args, **kwargs)
        token_storage = LoginTokenStorage(self.request.user)
        c = OutlookConnection(
            get_local_key("o365_login_app_settings.o365_app_client_id"),
            get_local_key("o365_login_app_settings.o365_app_secret"),
            token_storage,
            redirect_url='https://%s/django_outlook/login_result/' % self.request.get_host()
        )
        auth_url = c.get_auth_url()
        return auth_url


class OutlookLoginResultView(TemplateView):
    template_name = 'django_outlook/key_got.html'

    def get_context_data(self, **kwargs):
        # return super(OutlookLoginResultView, self).get_context_data(**kwargs)
        # param = retrieve_param(self.request)
        token_storage = LoginTokenStorage(self.request.user)
        c = OutlookConnection(
            get_local_key("o365_login_app_settings.o365_app_client_id"),
            get_local_key("o365_login_app_settings.o365_app_secret"),
            token_storage,
            redirect_url='https://%s/django_outlook/login_result/' % self.request.get_host()
        )
        token_url = "%s/?%s" % ("https://localhost", self.request.META['QUERY_STRING'])
        param = retrieve_param(self.request)
        res = c.update_extra_data(token_url, param["state"])
        return res
