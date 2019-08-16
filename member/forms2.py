from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Profile


class MemberSignupForm(forms.Form):
    first_name = forms.CharField(
        label=_('First name'),
        max_length=30,
        widget=forms.TextInput(),
    )

    last_name = forms.CharField(
        label=_('Last name'),
        max_length=30,
        widget=forms.TextInput(),
    )

    terms = forms.BooleanField(
        label=_('I agree to Terms and Conditions.'),
    )

    privacy = forms.BooleanField(
        label=_('I agree to Privacy Policy.'),
    )

    def signup(self, request, user):
        # Required fields for Django default model
        user.first_name = self.cleaned_data['first_name'].strip()
        user.last_name = self.cleaned_data['last_name'].strip()
        user.save()

        # Required fields for profile model
        profile = Profile()
        profile.user = user
        profile.save()
