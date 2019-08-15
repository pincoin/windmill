from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import (
    TimeStampedModel
)


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

    class Meta:
        verbose_name = _('Golf club')
        verbose_name_plural = _('Golf clubs')

    def __str__(self):
        return '{} {} {}'.format(self.title, self.email, self.phone)
