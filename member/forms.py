from allauth.account import forms as allauth_forms
from django import forms
from django.utils.timezone import (
    now, timedelta
)
from django.utils.translation import ugettext_lazy as _

from conf.formmixins import GoogleRecaptchaMixin
from . import settings as member_settings


class MemberLoginForm(GoogleRecaptchaMixin, allauth_forms.LoginForm):
    def __init__(self, *args, **kwargs):
        self.recaptcha = kwargs.pop('recaptcha', None)
        super(MemberLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.recaptcha \
                and self.user and self.user.last_login \
                and now() - self.user.last_login > timedelta(days=member_settings.DAYS_LOGIN_RECPATCHA):
            raise forms.ValidationError(_("You haven't logged for {} days.")
                                        .format(member_settings.DAYS_LOGIN_RECPATCHA))

        if self.recaptcha:
            self.validate_google_recaptcha()

        cleaned_data = super(MemberLoginForm, self).clean()
        return cleaned_data


class MemberUnregisterForm(forms.Form):
    agree = forms.BooleanField(
        label=_('I really would like to unregister.'),
        widget=forms.CheckboxInput(),
    )


class MemberAddEmailForm(allauth_forms.AddEmailForm):
    pass


class MemberChangePasswordForm(GoogleRecaptchaMixin, allauth_forms.ChangePasswordForm):
    def clean(self):
        self.validate_google_recaptcha()

        cleaned_data = super(MemberChangePasswordForm, self).clean()
        return cleaned_data


class MemberSetPasswordForm(GoogleRecaptchaMixin, allauth_forms.SetPasswordForm):
    def clean(self):
        self.validate_google_recaptcha()

        cleaned_data = super(MemberSetPasswordForm, self).clean()
        return cleaned_data


class MemberResetPasswordForm(GoogleRecaptchaMixin, allauth_forms.ResetPasswordForm):
    def clean(self):
        self.validate_google_recaptcha()

        cleaned_data = super(MemberResetPasswordForm, self).clean()
        return cleaned_data


class MemberResetPasswordKeyForm(allauth_forms.ResetPasswordKeyForm):
    pass

