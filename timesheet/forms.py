from django import forms

from . import models


class PunchLogForm(forms.ModelForm):
    latitude = forms.DecimalField(widget=forms.HiddenInput())

    longitude = forms.DecimalField(widget=forms.HiddenInput())

    class Meta:
        model = models.PunchLog
        fields = ()
