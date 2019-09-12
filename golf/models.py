import re
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models  as model_utils_models


class Holiday(model_utils_models.TimeStampedModel):
    COUNTRY_CHOICES = Choices(
        (1, 'thailand', _('Thailand')),
        (2, 'south_korea', _('South Korea')),
        (3, 'japan', _('Japan')),
        (4, 'china', _('China')),
    )

    title = models.CharField(
        verbose_name=_('Holiday name'),
        max_length=255,
    )

    holiday = models.DateField(
        verbose_name=_('Holiday day'),
        db_index=True,
    )

    country = models.IntegerField(
        verbose_name=_('Country code'),
        choices=COUNTRY_CHOICES,
        default=COUNTRY_CHOICES.thailand,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Holiday')
        verbose_name_plural = _('Holidays')

        unique_together = ('holiday', 'country')

    def __str__(self):
        return '{} {} {}'.format(self.title, self.holiday, self.country)


class Agency(model_utils_models.TimeStampedModel):
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

    memo = models.TextField(
        verbose_name=_('Memo'),
        help_text=_('A short description'),
        blank=True,
        null=True,
    )

    products = models.ManyToManyField(
        'golf.ClubProductListMembership',
        through='golf.AgencyClubProductListMembership'
    )

    class Meta:
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')

    def __str__(self):
        return '{} {} {}'.format(self.title, self.email, self.phone)


class ClubProduct(model_utils_models.TimeStampedModel):
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


class Club(model_utils_models.TimeStampedModel):
    HOLE_CHOICES = Choices(
        (0, 'eighteen', _('18 Holes')),
        (1, 'nine', _('9 Holes')),
        (2, 'twentyseven', _('27 Holes')),
        (3, 'thirtysix', _('36 Holes')),
    )

    COUNTRY_CHOICES = Choices(
        (1, 'thailand', _('Thailand')),
        (2, 'south_korea', _('South Korea')),
        (3, 'japan', _('Japan')),
        (4, 'china', _('China')),
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

    high_season = models.IntegerField(
        verbose_name=_('High season'),
        default=0x0C03,  # b'110000000011'
    )

    max_high_weekday = models.PositiveIntegerField(
        verbose_name=_('Max # of High/Weekday'),
        default=0,
    )

    max_high_weekend = models.PositiveIntegerField(
        verbose_name=_('Max # of High/Weekend'),
        default=0,
    )

    max_low_weekday = models.PositiveIntegerField(
        verbose_name=_('Max # of Low/Weekday'),
        default=0,
    )

    max_low_weekend = models.PositiveIntegerField(
        verbose_name=_('Max # of Low/Weekday'),
        default=0,
    )

    country = models.IntegerField(
        verbose_name=_('Country code'),
        choices=COUNTRY_CHOICES,
        default=COUNTRY_CHOICES.thailand,
        db_index=True,
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

    def __str__(self):
        return '{} - {}'.format(self.club.title, self.product_list)


class AgencyClubProductListMembership(models.Model):
    agency = models.ForeignKey(
        'golf.Agency',
        verbose_name=_('Agency'),
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    product_list = models.ForeignKey(
        'golf.ClubProductListMembership',
        verbose_name=_('Product list'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    fee = models.DecimalField(
        verbose_name=_('Fee amount'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
    )

    class Meta:
        verbose_name = _('Agency product list membership')
        verbose_name_plural = _('Agency product list membership')

        unique_together = ('agency', 'product_list')

    def __str__(self):
        return '{} {}'.format(self.agency.title, self.product_list)


class AgentProfile(model_utils_models.TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        db_index=True,
        on_delete=models.CASCADE,
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

    @property
    def fullname(self):
        pattern = re.compile(r'^[가-힣]+$')  # Only Hangul

        if pattern.match(self.user.last_name) and pattern.match(self.user.first_name):
            return '{}{}'.format(self.user.last_name, self.user.first_name)
        else:
            return '{} {}'.format(self.user.first_name, self.user.last_name)


class Deposit(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    agency = models.ForeignKey(
        'golf.Agency',
        verbose_name=_('Agency'),
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    amount = models.DecimalField(
        verbose_name=_('Amount'),
        help_text=_('THB'),
        max_digits=11,
        decimal_places=2,
    )

    received = models.DateTimeField(
        verbose_name=_('Received date'),
    )

    class Meta:
        verbose_name = _('Deposit')
        verbose_name_plural = _('Deposits')

    def __str__(self):
        return 'agency - {} / payment - {} {}'.format(
            self.agency.title, self.amount, self.received
        )


class Booking(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
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

    STATUS_CHOICES = Choices(
        (0, 'order_opened', _('order opened')),
        (1, 'order_pending', _('order pending')),
        (2, 'payment_pending', _('payment pending')),
        (3, 'completed', _('order complete')),
        (4, 'offered', _('order offered')),
        (5, 'voided', _('order voided')),
        (6, 'refund_requested', _('refund requested')),
        (7, 'refund_pending', _('refund pending')),
        (8, 'refunded1', _('order refunded(original)')),  # original order
        (9, 'refunded2', _('order refunded(reverse)')),  # refund order
    )

    booking_uuid = models.UUIDField(
        verbose_name=_('UUID'),
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    club = models.ForeignKey(
        'golf.Club',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    agency = models.ForeignKey(
        'golf.Agency',
        verbose_name=_('Agency'),
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Agent'),
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    round_date = models.DateField(
        verbose_name=_('Round day'),
        db_index=True,
    )

    round_time = models.TimeField(
        verbose_name=_('Round time'),
    )

    tee_off_time = models.TimeField(
        verbose_name=_('Tee off time'),
        null=True,
        blank=True,
    )

    people = models.IntegerField(
        verbose_name=_('No. of people'),
    )

    fee = models.DecimalField(
        verbose_name=_('Fee amount'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=255,
    )

    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=255,
    )

    fullname = models.CharField(
        verbose_name=_('Full name'),
        max_length=255,
    )

    memo = models.TextField(
        verbose_name=_('Memo'),
        blank=True,
        null=True,
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

    status = models.IntegerField(
        verbose_name=_('Booking status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.order_opened,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Booking')

    def __str__(self):
        return '{}-{} {}-{}'.format(self.booking_uuid, self.first_name, self.last_name, self.agency.title)


class BookingTeeOffTime(model_utils_models.TimeStampedModel):
    STATUS_CHOICES = Choices(
        (0, 'offered', _('Time offered')),
        (1, 'accepted', _('Time accepted')),
        (2, 'rejected', _('Time rejected')),
        (3, 'revoked', _('Time revoked')),
        (4, 'voided', _('Time voided')),
    )

    booking = models.ForeignKey(
        'golf.Booking',
        verbose_name=_('Booking'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    tee_off_time = models.TimeField(
        verbose_name=_('Tee-off time'),
    )

    status = models.IntegerField(
        verbose_name=_('Tee-off time status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.offered,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Tee-off time')
        verbose_name_plural = _('Tee-off time')

        ordering = ('-tee_off_time',)

        unique_together = ('booking', 'tee_off_time')

    def __str__(self):
        return '{}-{}'.format(self.booking.booking_uuid, self.tee_off_time)


class BookingCounter(model_utils_models.TimeStampedModel):
    DAY_CHOICES = Choices(
        (0, 'high_weekday', _('High/Weekday')),
        (1, 'high_weekend', _('High/Weekend')),
        (2, 'low_weekday', _('Low/Weekday')),
        (3, 'low_weekend', _('Low/Weekend')),
    )

    club = models.ForeignKey(
        'golf.Club',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    booking_date = models.DateField(
        verbose_name=_('Booking date'),
        db_index=True,
    )

    counter = models.PositiveIntegerField(
        verbose_name=_('Booking counter'),
        default=0,
        db_index=True,
    )

    day_of_week = models.IntegerField(
        verbose_name=_('Season / Day of week'),
        choices=DAY_CHOICES,
        default=DAY_CHOICES.high_weekday,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Booking counter')
        verbose_name_plural = _('Booking counters')

        ordering = ('-booking_date',)

        unique_together = ('club', 'booking_date')

    def __str__(self):
        return '{} {} {}'.format(self.club.title, self.booking_date, self.counter)


class BookingPayment(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    ACCOUNT_CHOICES = Choices(
        (0, 'kasikorn', _('Kasikorn Bank')),
        (1, 'bangkok', _('Bangkok Bank')),
        (2, 'scb', _('Siam Commercial Bank')),
        (3, 'ayudhya', _('Ayudhya Bank')),
        (4, 'krungthai', _('Krungthai Bank')),
    )

    booking = models.ForeignKey(
        'golf.Booking',
        verbose_name=_('Booking'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    account = models.IntegerField(
        verbose_name=_('Bank account'),
        choices=ACCOUNT_CHOICES,
        default=ACCOUNT_CHOICES.kasikorn,
        db_index=True,
    )

    amount = models.DecimalField(
        verbose_name=_('Paid amount'),
        max_digits=11,
        decimal_places=2,
    )

    received = models.DateTimeField(
        verbose_name=_('Received date'),
    )

    class Meta:
        verbose_name = _('Booking payment')
        verbose_name_plural = _('Booking payments')

    def __str__(self):
        return 'booking - {} / payment - {} {} {}'.format(
            self.booking.booking_uuid, self.account, self.amount, self.received
        )


class BookingAccountReceivable(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    booking = models.ForeignKey(
        'golf.Booking',
        verbose_name=_('Booking'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    amount = models.DecimalField(
        verbose_name=_('Unpaid mount'),
        max_digits=11,
        decimal_places=2,
    )

    class Meta:
        verbose_name = _('Booking account receivable')
        verbose_name_plural = _('Booking accounts receivable')

    def __str__(self):
        return 'booking - {} / account receivable - {}'.format(self.booking.booking_uuid, self.amount)


class BookingChangeLog(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    booking = models.ForeignKey(
        'golf.Booking',
        verbose_name=_('Booking'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    log = models.TextField(
        verbose_name=_('Changelog'),
    )

    memo = models.TextField(
        verbose_name=_('Memo'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Booking change log')
        verbose_name_plural = _('Booking change logs')

    def __str__(self):
        return 'booking - {} / log - {} '.format(self.booking.booking_uuid, self.log)


'''
class PriceTable(TimeStampedModel):
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
'''
