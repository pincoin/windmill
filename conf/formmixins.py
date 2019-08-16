import json
import urllib

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class GoogleRecaptchaMixin:
    def validate_google_recaptcha(self):
        captcha_response = self.data.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA['secret_key'],
            'response': captcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        captcha_response = urllib.request.urlopen(req)
        result = json.loads(captcha_response.read().decode())

        if not result['success']:
            raise forms.ValidationError(_('Invalid reCAPTCHA. Please try again.'))

    class Media:
        js = ('https://www.google.com/recaptcha/api.js',)
