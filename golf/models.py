from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel


class TravelAgent(TimeStampedModel):
    title = models.CharField(
        verbose_name=_('Travel agent name'),
        max_length=255,
    )

    bank_account = models.CharField(
        verbose_name=_('Bank account'),
        max_length=255,
        blank=True,
        null=True,
    )

    phone = models.CharField(
        verbose_name=_('Phone number'),
        max_length=16,
    )

    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
    )

    website = models.URLField(
        verbose_name=_('Website'),
        max_length=255,
        blank=True,
        null=True,
    )

    deposit = models.DecimalField(
        verbose_name=_('Deposit amount'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    memo = models.TextField(
        verbose_name=_('Memo'),
        help_text=_('A short description'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Travel agent')
        verbose_name_plural = _('Travel agents')

    def __str__(self):
        return '{} {} {}'.format(self.title, self.email, self.phone)


class GolfClub(TimeStampedModel):
    HOLE_CHOICES = Choices(
        (0, 'eighteen', _('18 Holes')),
        (1, 'nine', _('9 Holes')),
    )

    title = models.CharField(
        verbose_name=_('Golf club name'),
        max_length=255,
    )

    phone = models.CharField(
        verbose_name=_('Phone number'),
        max_length=16,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        blank=True,
        null=True,
    )

    website = models.URLField(
        verbose_name=_('Website'),
        max_length=255,
        blank=True,
        null=True,
    )

    hole = models.IntegerField(
        verbose_name=_('No. of Holes'),
        choices=HOLE_CHOICES,
        default=HOLE_CHOICES.eighteen,
        db_index=True,
    )

    cart_rental_required = models.BooleanField(
        verbose_name=_('Cart rental required'),
        default=False,
        db_index=True,
    )

    cart_fee = models.DecimalField(
        verbose_name=_('Cart fee'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    caddie_fee = models.DecimalField(
        verbose_name=_('Caddie fee'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    class Meta:
        verbose_name = _('Golf club')
        verbose_name_plural = _('Golf clubs')

    def __str__(self):
        return '{} {} {}'.format(self.title, self.email, self.phone)


class PriceTable(TimeStampedModel):
    SEASON_CHOICES = Choices(
        (0, 'low', _('Low season')),
        (1, 'high', _('High season')),
    )

    DAY_CHOICES = Choices(
        (0, 'weekday', _('Weekday')),
        (1, 'weekend', _('Weekend')),
    )

    SLOT_CHOICES = Choices(
        (0, 'twilight', _('Twilight')),
        (1, 'morning', _('Morning')),
        (2, 'daytime', _('Daytime')),
        (3, 'night', _('Night')),
    )

    company = models.ForeignKey(
        'golf.TravelAgent',
        verbose_name=_('Travel agent'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    club = models.ForeignKey(
        'golf.GolfClub',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    season = models.IntegerField(
        verbose_name=_('High/Low Season'),
        choices=SEASON_CHOICES,
        default=SEASON_CHOICES.high,
        db_index=True,
    )

    day_of_week = models.IntegerField(
        verbose_name=_('Day of week'),
        choices=DAY_CHOICES,
        default=DAY_CHOICES.weekday,
        db_index=True,
    )

    slot = models.IntegerField(
        verbose_name=_('Time slot'),
        choices=SLOT_CHOICES,
        default=SLOT_CHOICES.twilight,
        db_index=True,
    )

    fee = models.DecimalField(
        verbose_name=_('Fee amount'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    cost = models.DecimalField(
        verbose_name=_('Cost amount'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    @property
    def profit(self):
        return self.fee - self.cost

    class Meta:
        verbose_name = _('Price table')
        verbose_name_plural = _('Price tables')

    def __str__(self):
        return '{} {} {}'.format(self.company.title, self.club.title, self.fee)
