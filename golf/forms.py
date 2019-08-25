from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class BookingSearchForm(forms.Form):
    category = forms.ChoiceField(
        choices=(
            ('1', _('Booking person'),),
            ('2', _('Memo'),),
        ),
        widget=forms.Select(
            attrs={
                'class': 'input',
                'required': 'True',
            }
        )
    )

    keyword = forms.CharField(
        label=_('Search word'),
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': _('Search word'),
                'required': 'True',
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', '1')
        keyword = kwargs.pop('keyword', '')

        super(BookingSearchForm, self).__init__(*args, **kwargs)

        self.fields['category'].initial = category
        self.fields['keyword'].initial = keyword


class BookingStatusSearchForm(forms.Form):
    status = forms.ChoiceField(
        choices=models.Booking.STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                'required': 'True',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        status = kwargs.pop('status', '0')

        super(BookingStatusSearchForm, self).__init__(*args, **kwargs)

        self.fields['status'].initial = status


class BookingGolfClubSearchForm(forms.Form):
    club = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'required': 'True',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        club = kwargs.pop('club', '0')

        super(BookingGolfClubSearchForm, self).__init__(*args, **kwargs)

        self.fields['club'].initial = club
        self.fields['club'].choices = [(c.id, str(c.title)) for c in models.Club.objects.all()]


class BookingAgencySearchForm(forms.Form):
    agency = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'required': 'True',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        agency = kwargs.pop('agency', '0')

        super(BookingAgencySearchForm, self).__init__(*args, **kwargs)

        self.fields['agency'].initial = agency
        self.fields['agency'].choices = [(a.id, str(a.title)) for a in models.Agency.objects.all()]
