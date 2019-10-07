from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models  as model_utils_models


class TimeSheet(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Staff'),
        db_index=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = _('Time sheet')
        verbose_name_plural = _('Time sheets')

    def __str__(self):
        return '{}-{}'.format(self.staff.first_name, self.staff.last_name)

    @property
    def regular_hours(self):
        return ''

    @property
    def overtime_hours(self):
        return ''

    @property
    def total_hours(self):
        return ''


class PunchLog(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    STATUS_CHOICES = Choices(
        (0, 'punch_in', _('Punch-in')),
        (1, 'punch_out', _('Punch-out')),
    )

    sheet = models.ForeignKey(
        'timesheet.TimeSheet',
        verbose_name=_('Time sheet'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    status = models.IntegerField(
        verbose_name=_('Punch status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.punch_in,
        db_index=True,
    )

    punch_time = models.DateTimeField(
        verbose_name=_('Punch time'),
    )

    latitude = models.DecimalField(
        verbose_name=_('Punch latitude'),
        max_digits=22,
        decimal_places=16,
    )

    longitude = models.DecimalField(
        verbose_name=_('Punch longitude'),
        max_digits=22,
        decimal_places=16,
    )

    user_agent = models.TextField(
        verbose_name=_('user-agent'),
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
    )

    memo = models.TextField(
        verbose_name=_('Memo'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Punch log')
        verbose_name_plural = _('Punch logs')
