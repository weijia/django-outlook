# from allauth.account.forms import LoginForm
# from allauth.socialaccount.providers.openid.forms import LoginForm
from cms.test_utils.project.sampleapp.forms import LoginForm
from django.views.generic import FormView
# from django_th.forms.base import LoginForm


class OutlookLoginFormView(FormView):
    form_class = LoginForm

    def form_valid(self, form):
        return super(OutlookLoginFormView, self).form_valid(form)

