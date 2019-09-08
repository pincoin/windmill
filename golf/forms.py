from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.template.defaultfilters import date as _date
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import fields
from . import models


class DummyForm(forms.Form):
    pass


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

        cache_key = 'golf.all_clubs'
        cache_time = settings.CACHES['default']['TIMEOUT']

        clubs = cache.get(cache_key)

        if not clubs:
            clubs = models.Club.objects.all()
            cache.set(cache_key, clubs, cache_time)

        self.fields['club'].initial = club
        self.fields['club'].choices = [(c.id, str(c.title)) for c in clubs]


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

        cache_key = 'golf.all_agencies'
        cache_time = settings.CACHES['default']['TIMEOUT']

        agencies = cache.get(cache_key)

        if not agencies:
            agencies = models.Agency.objects.all()
            cache.set(cache_key, agencies, cache_time)

        self.fields['agency'].initial = agency
        self.fields['agency'].choices = [(a.id, str(a.title)) for a in agencies]


class BookingForm(forms.ModelForm):
    club = fields.GolfClubChoiceField(
        queryset=None,
        label=_('Golf club'),
        widget=forms.Select(
            attrs={
                'class': 'input',
                'required': 'True',
            }
        ),
    )

    slot = forms.ChoiceField(
        label=_('Time slot'),
        choices=models.Booking.SLOT_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'input',
                'required': 'True',
            }
        )
    )

    round_date = forms.CharField(
        label=_('Round date/time'),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'required': 'True',
                'placeholder': _date(timezone.make_aware(timezone.localtime().now()), 'Y-m-d (l)')
            }),
    )

    round_time_hour = forms.ChoiceField(
        choices=(
            ('6', '06',),
            ('7', '07',),
            ('8', '08',),
            ('9', '09',),
            ('10', '10',),
            ('11', '11',),
            ('12', '12',),
            ('13', '13',),
            ('14', '14',),
            ('15', '15',),
            ('16', '16',),
            ('17', '17',),
            ('18', '18',),
            ('19', '19',),
            ('20', '20',),
        ),
        widget=forms.Select(
            attrs={
                'class': 'input',
                'required': 'True',
            }),
    )

    round_time_minute = forms.ChoiceField(
        choices=(
            ('0', '00',),
            ('10', '10',),
            ('20', '20',),
            ('30', '30',),
            ('40', '40',),
            ('50', '50',),
        ),
        widget=forms.Select(
            attrs={
                'class': 'input',
                'required': 'True',
            }),
    )

    people = forms.ChoiceField(
        label=_('No. of people'),
        choices=(
            ('1', '1',),
            ('2', '2',),
            ('3', '3',),
            ('4', '4',),
            ('5', '5',),
        ),
        widget=forms.Select(
            attrs={
                'class': 'input',
                'required': 'True',
            }
        )
    )

    first_name = forms.CharField(
        label=_('Full name (Passport)'),
        max_length=255,
        validators=[RegexValidator(r'^[a-zA-Z]+$', _('Only alphabets are allowed.'))],
        widget=forms.TextInput(
            attrs={
                'placeholder': _('First name'),
                'class': 'input',
            }),
    )

    last_name = forms.CharField(
        max_length=255,
        validators=[RegexValidator(r'^[a-zA-Z]+$', _('Only alphabets are allowed.'))],
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Last name'),
                'class': 'input',
            }),
    )

    memo = forms.CharField(
        label=_('Memo'),
        required=False,
        max_length=2000,
        widget=forms.Textarea(
            attrs={
                'placeholder': _('Remarks'),
                'class': 'textarea',
            }),
    )

    def __init__(self, *args, **kwargs):
        club = kwargs.pop('club', '1')

        super(BookingForm, self).__init__(*args, **kwargs)

        cache_key = 'golf.all_clubs'
        cache_time = settings.CACHES['default']['TIMEOUT']

        clubs = cache.get(cache_key)

        if not clubs:
            clubs = models.Club.objects.all()
            cache.set(cache_key, clubs, cache_time)

        self.fields['club'].queryset = clubs
        self.fields['club'].initial = club

    class Meta:
        model = models.Booking
        fields = ('club', 'slot', 'round_date', 'people', 'first_name', 'last_name', 'memo')

    def clean_round_date(self):
        return self.cleaned_data['round_date'][0:10]

    def clean(self):
        if not (timezone.make_aware(timezone.localtime().now())
                < timezone.make_aware(timezone.datetime.strptime(self.cleaned_data['round_date'], '%Y-%m-%d'))
                < timezone.make_aware(timezone.localtime().now()) + timezone.timedelta(days=365)):
            raise forms.ValidationError(_('Invalid round date'))

        if int(self.cleaned_data['slot']) == models.Booking.SLOT_CHOICES.morning \
                and int(self.cleaned_data['round_time_hour']) not in [6, 7, 8, 9, 10, 11] \
                or int(self.cleaned_data['slot']) == models.Booking.SLOT_CHOICES.daytime \
                and int(self.cleaned_data['round_time_hour']) not in [11, 12, 13, 14] \
                or int(self.cleaned_data['slot']) == models.Booking.SLOT_CHOICES.twilight \
                and int(self.cleaned_data['round_time_hour']) not in [15, ] \
                or int(self.cleaned_data['slot']) == models.Booking.SLOT_CHOICES.night \
                and int(self.cleaned_data['round_time_hour']) not in [16, 17, 18, 19]:
            raise forms.ValidationError(_('Invalid round time'))


class FeeForm(forms.Form):
    club_id = forms.IntegerField()

    agency_id = forms.IntegerField()

    round_date = forms.CharField(
        max_length=255,
        validators=[RegexValidator(r'\d{4}-\d{2}-\d{2}', _('YYYY-MM-DD'))],
    )

    slot = forms.ChoiceField(
        choices=models.Booking.SLOT_CHOICES,
    )

    def clean(self):
        if not (timezone.make_aware(timezone.localtime().now())
                < timezone.make_aware(timezone.datetime.strptime(self.cleaned_data['round_date'], '%Y-%m-%d'))
                < timezone.make_aware(timezone.localtime().now()) + timezone.timedelta(days=365)):
            raise forms.ValidationError(_('Invalid round date'))
