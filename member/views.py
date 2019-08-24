import uuid

from allauth.account import views as allauth_views
from allauth.account.models import EmailAddress
from allauth.socialaccount import views as socialaccount_views
from django.conf import settings
from django.contrib.auth import (
    get_user_model, logout)
from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic

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
        context['page_title'] = _('Sign Up')
        return context


class MemberAccountInactiveView(allauth_views.AccountInactiveView):
    template_name = 'member/account/account_inactive.html'

    def get_context_data(self, **kwargs):
        context = super(MemberAccountInactiveView, self).get_context_data(**kwargs)
        context['page_title'] = _('Account Inactive')
        return context


class MemberUnregisterView(auth_mixins.AccessMixin, generic.FormView):
    template_name = 'member/account/unregister.html'
    form_class = forms.MemberUnregisterForm

    def dispatch(self, request, *args, **kwargs):
        # LoginRequiredMixin is not used because of inheritance order
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        self.member = get_user_model().objects.get(pk=self.request.user.id)

        return super(MemberUnregisterView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberUnregisterView, self).get_context_data(**kwargs)
        context['page_title'] = _('Unregister')
        context['member'] = self.member
        return context

    def form_valid(self, form):
        response = super(MemberUnregisterView, self).form_valid(form)

        self.member.email = self.member.email + '_' + str(uuid.uuid4())
        self.member.username = self.member.username + '_' + str(uuid.uuid4())
        self.member.password = ''
        self.member.is_active = False
        self.member.is_staff = False
        self.member.is_superuser = False
        self.member.save()

        EmailAddress.objects.filter(user__id=self.member.id).delete()

        # SocialAccount.objects.filter(user__id=self.member.id).delete()

        logout(self.request)

        return response

    def get_success_url(self):
        return reverse('home')


class MemberPasswordChangeView(auth_mixins.LoginRequiredMixin, allauth_views.PasswordChangeView):
    template_name = 'member/account/password_change.html'
    form_class = forms.MemberChangePasswordForm

    def form_invalid(self, form):
        for field in form.errors.keys():
            if field is not '__all__':
                form.fields[field].widget.attrs['class'] = 'input is-danger'
        return super(MemberPasswordChangeView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(MemberPasswordChangeView, self).get_context_data(**kwargs)
        context['google_recaptcha_site_key'] = settings.GOOGLE_RECAPTCHA['site_key']
        context['page_title'] = _('Password Change')
        return context


class MemberPasswordSetView(auth_mixins.LoginRequiredMixin, allauth_views.PasswordSetView):
    template_name = 'member/account/password_set.html'
    form_class = forms.MemberSetPasswordForm

    def form_invalid(self, form):
        for field in form.errors.keys():
            if field is not '__all__':
                form.fields[field].widget.attrs['class'] = 'input is-danger'
        return super(MemberPasswordSetView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(MemberPasswordSetView, self).get_context_data(**kwargs)
        context['page_title'] = _('Password Set')
        context['google_recaptcha_site_key'] = settings.GOOGLE_RECAPTCHA['site_key']
        return context


class MemberPasswordReset(allauth_views.PasswordResetView):
    template_name = 'member/account/password_reset.html'
    form_class = forms.MemberResetPasswordForm

    def form_invalid(self, form):
        for field in form.errors.keys():
            if field is not '__all__':
                form.fields[field].widget.attrs['class'] = 'input is-danger'
        return super(MemberPasswordReset, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(MemberPasswordReset, self).get_context_data(**kwargs)
        context['page_title'] = _('Password Reset')
        context['google_recaptcha_site_key'] = settings.GOOGLE_RECAPTCHA['site_key']
        return context


class MemberPasswordResetDoneView(allauth_views.PasswordResetDoneView):
    template_name = 'member/account/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super(MemberPasswordResetDoneView, self).get_context_data(**kwargs)
        context['page_title'] = _('Password Reset Done')
        return context


class MemberPasswordResetFromKeyView(allauth_views.PasswordResetFromKeyView):
    template_name = 'member/account/password_reset_from_key.html'
    form_class = forms.MemberResetPasswordKeyForm

    def form_invalid(self, form):
        for field in form.errors.keys():
            if field is not '__all__':
                form.fields[field].widget.attrs['class'] = 'input is-danger'
        return super(MemberPasswordResetFromKeyView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(MemberPasswordResetFromKeyView, self).get_context_data(**kwargs)
        context['page_title'] = _('Password Reset')
        return context


class MemberPasswordResetFromKeyDoneView(allauth_views.PasswordResetFromKeyDoneView):
    template_name = 'member/account/password_reset_from_key_done.html'

    def get_context_data(self, **kwargs):
        context = super(MemberPasswordResetFromKeyDoneView, self).get_context_data(**kwargs)
        context['page_title'] = _('Password Reset Done')
        return context


class MemberEmailVerificationSentView(allauth_views.EmailVerificationSentView):
    template_name = 'member/account/verification_sent.html'

    def get_context_data(self, **kwargs):
        context = super(MemberEmailVerificationSentView, self).get_context_data(**kwargs)
        context['page_title'] = _('Email Verification Sent')
        return context


class MemberConfirmEmailView(allauth_views.ConfirmEmailView):
    template_name = 'member/account/email_confirm.html'

    def get_context_data(self, **kwargs):
        context = super(MemberConfirmEmailView, self).get_context_data(**kwargs)
        context['page_title'] = _('Confirm Email Request')
        return context


class MemberEmailView(auth_mixins.LoginRequiredMixin, allauth_views.EmailView):
    template_name = 'member/account/email.html'
    form_class = forms.MemberAddEmailForm

    def get_context_data(self, **kwargs):
        context = super(MemberEmailView, self).get_context_data(**kwargs)
        context['page_title'] = _('Email Management')
        return context


class MemberSocialLoginCancelledView(socialaccount_views.LoginCancelledView):
    template_name = 'member/socialaccount/login_cancelled.html'

    def get_context_data(self, **kwargs):
        context = super(MemberSocialLoginCancelledView, self).get_context_data(**kwargs)
        context['page_title'] = _('Login Cancelled')
        return context


class MemberSocialLoginErrorView(socialaccount_views.LoginErrorView):
    template_name = 'member/socialaccount/authentication_error.html'

    def get_context_data(self, **kwargs):
        context = super(MemberSocialLoginErrorView, self).get_context_data(**kwargs)
        context['page_title'] = _('Social Network Login Failure')
        return context


class MemberSocialSignupView(socialaccount_views.SignupView):
    template_name = 'member/socialaccount/signup.html'

    def get_context_data(self, **kwargs):
        context = super(MemberSocialSignupView, self).get_context_data(**kwargs)
        context['page_title'] = _('Sign Up')
        return context


class MemberSocialConnectionsView(auth_mixins.LoginRequiredMixin, socialaccount_views.ConnectionsView):
    template_name = 'member/socialaccount/connections.html'

    def get_context_data(self, **kwargs):
        context = super(MemberSocialConnectionsView, self).get_context_data(**kwargs)
        context['page_title'] = _('Connect with SNS accounts')
        return context


class MemberProfileView(auth_mixins.LoginRequiredMixin, generic.DetailView):
    template_name = 'member/account/profile.html'
    context_object_name = 'member'

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        return get_user_model().objects \
            .prefetch_related('agentprofile', 'agentprofile__agency') \
            .get(pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(MemberProfileView, self).get_context_data(**kwargs)
        context['page_title'] = _('Profile')
        return context


class MemberOrganizationCreateView(generic.CreateView):
    template_name = 'member/account/organization.html'
    form_class = forms.OrganizationForm

    def get_form_kwargs(self):
        kwargs = super(MemberOrganizationCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(MemberOrganizationCreateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Organization application')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(MemberOrganizationCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('account_organization')
