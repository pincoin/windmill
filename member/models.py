from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import (
    TimeStampedModel
)


class Profile(TimeStampedModel):
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
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return '{} {} {}'.format(self.user.email, self.user.username, self.cellphone)


class LoginLog(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
    )

    class Meta:
        verbose_name = _('Login log')
        verbose_name_plural = _('Login logs')

    def __str__(self):
        return '{} {} {}'.format(self.user.email, self.ip_address, self.created)
