from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel


class Agency(TimeStampedModel):
    AGENCY_TYPE_CHOICES = Choices(
        (0, 'travel', _('Travel agency')),
        (1, 'personal', _('Personal agent')),
        (2, 'booking', _('Booking agency')),
    )

    title = models.CharField(
        verbose_name=_('Agency name'),
        max_length=255,
    )

    agency_type = models.IntegerField(
        verbose_name=_('Agency type'),
        choices=AGENCY_TYPE_CHOICES,
        default=AGENCY_TYPE_CHOICES.travel,
        db_index=True,
    )

    bank_account = models.CharField(
        verbose_name=_('Bank account'),
        max_length=255,
        blank=True,
        null=True,
    )

    cancellable_days = models.IntegerField(
        verbose_name=_('Cancellable days'),
        db_index=True,
        default=3,
    )

    due_days = models.IntegerField(
        verbose_name=_('Payment due days'),
        db_index=True,
        default=1,
    )

    bookable_days = models.IntegerField(
        verbose_name=_('Bookable days'),
        db_index=True,
        default=90,
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
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')

    def __str__(self):
        return '{} {} {}'.format(self.title, self.email, self.phone)


class ClubProduct(TimeStampedModel):
    SEASON_CHOICES = Choices(
        (0, 'low', _('Low season')),
        (1, 'high', _('High season')),
    )

    DAY_CHOICES = Choices(
        (0, 'weekday', _('Weekday')),
        (1, 'weekend', _('Weekend')),
    )

    SLOT_CHOICES = Choices(
        (0, 'morning', _('Morning')),
        (1, 'daytime', _('Daytime')),
        (2, 'twilight', _('Twilight')),
        (3, 'night', _('Night')),
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
        default=SLOT_CHOICES.morning,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Golf club product')
        verbose_name_plural = _('Golf club products')

        unique_together = ('season', 'day_of_week', 'slot')

    def __str__(self):
        return '{} / {} / {}'.format(
            self.SEASON_CHOICES[self.season],
            self.DAY_CHOICES[self.day_of_week],
            self.SLOT_CHOICES[self.slot],
        )


class Club(TimeStampedModel):
    HOLE_CHOICES = Choices(
        (0, 'eighteen', _('18 Holes')),
        (1, 'nine', _('9 Holes')),
        (2, 'twentyseven', _('27 Holes')),
        (3, 'thirtysix', _('36 Holes')),
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

    products = models.ManyToManyField(
        'golf.ClubProduct',
        through='golf.ClubProductListMembership'
    )

    class Meta:
        verbose_name = _('Golf club')
        verbose_name_plural = _('Golf clubs')

    def __str__(self):
        return '{} {} {}'.format(self.title, self.email, self.phone)


class ClubProductListMembership(models.Model):
    club = models.ForeignKey(
        'golf.Club',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    product_list = models.ForeignKey(
        'golf.ClubProduct',
        verbose_name=_('Product list'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    start_time = models.TimeField(
        verbose_name=_('Start time'),
    )

    end_time = models.TimeField(
        verbose_name=_('End time'),
    )

    list_price = models.DecimalField(
        verbose_name=_('List price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
    )

    class Meta:
        verbose_name = _('Product list membership')
        verbose_name_plural = _('Product list membership')

        unique_together = ('club', 'product_list')


class AgentProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    agency = models.ForeignKey(
        'golf.Agency',
        verbose_name=_('Agency'),
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    cellphone = models.CharField(
        verbose_name=_('Cellphone number'),
        max_length=16,
        blank=True,
        null=True,
    )

    line_id = models.CharField(
        verbose_name=_('Line ID'),
        max_length=32,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Agent profile')
        verbose_name_plural = _('Agent profiles')

    def __str__(self):
        return '{} {} {}'.format(self.user.email, self.user.username, self.cellphone)

    def changeform_link(self):
        if self.id:
            # Replace "myapp" with the name of the app containing
            # your Certificate model:
            changeform_url = reverse(
                'admin:golf_profile_change', args=(self.id,)
            )
            return u'<a href="%s" target="_blank">Details</a>' % changeform_url
        return u''

    changeform_link.allow_tags = True
    changeform_link.short_description = ''  # omit column header


'''
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

    agency = models.ForeignKey(
        'golf.Agency',
        verbose_name=_('Agency'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    club = models.ForeignKey(
        'golf.Club',
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
        return '{} {} {}'.format(self.agency.title, self.club.title, self.fee)    
'''
