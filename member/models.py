from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel


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


class EmailBanned(TimeStampedModel):
    email = models.EmailField(
        verbose_name=_('Email address'),
    )

    class Meta:
        verbose_name = _('Banned Email Address')
        verbose_name_plural = _('Banned Email Addresses')

    def __str__(self):
        return '{} {}'.format(self.email, self.created)


class OrganizationApplication(TimeStampedModel):
    STATUS_CHOICES = Choices(
        (0, 'pending', _('Pending')),
        (1, 'complete', _('Complete')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        editable=True,
        on_delete=models.CASCADE,
    )

    message = models.TextField(
        verbose_name=_('Message'),
    )

    status = models.IntegerField(
        verbose_name=_('Status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.pending,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Organization application')
        verbose_name_plural = _('Organization applications')

    def __str__(self):
        return '{} {}'.format(self.user.id, self.created)
