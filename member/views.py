from allauth.account import views as allauth_views
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from . import forms
from . import settings as member_settings


class MemberLoginView(allauth_views.LoginView):
    template_name = 'member/account/login.html'
    form_class = forms.MemberLoginForm

    def get_form_kwargs(self):
        kwargs = super(MemberLoginView, self).get_form_kwargs()

        kwargs['recaptcha'] = False

        if member_settings.GOOGLE_RECAPTCHA_SESSION_KEY in self.request.session:
            kwargs['recaptcha'] = True

        return kwargs

    def form_valid(self, form):
        if member_settings.GOOGLE_RECAPTCHA_SESSION_KEY in self.request.session:
            del self.request.session[member_settings.GOOGLE_RECAPTCHA_SESSION_KEY]
        return super(MemberLoginView, self).form_valid(form)

    def form_invalid(self, form):
        self.request.session[member_settings.GOOGLE_RECAPTCHA_SESSION_KEY] = True
        self.request.session.modified = True
        return super(MemberLoginView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(MemberLoginView, self).get_context_data(**kwargs)
        context['page_title'] = _('Login')
        context['google_recaptcha_site_key'] = settings.GOOGLE_RECAPTCHA['site_key']
        return context


class MemberLogoutView(allauth_views.LogoutView):
    template_name = 'member/account/logout.html'

    def get_context_data(self, **kwargs):
        context = super(MemberLogoutView, self).get_context_data(**kwargs)
        context['page_title'] = _('Logout')
        return context



class MemberSignupView(allauth_views.SignupView):
    template_name = 'member/account/signup.html'

    def get_context_data(self, **kwargs):
        context = super(MemberSignupView, self).get_context_data(**kwargs)
        context['page_title'] = _('Sign up')
        return context