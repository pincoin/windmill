from allauth.account.signals import (
    user_logged_in, password_changed, password_reset, password_set
)
from django.dispatch import receiver
from ipware.ip import get_ip

from .models import LoginLog


@receiver(user_logged_in)
def login_logger(request, user, **kwargs):
    login_log = LoginLog()
    login_log.user = user
    login_log.ip_address = get_ip(request)
    login_log.save()


@receiver(password_changed)
def notify_password_changed(request, user, **kwargs):
    pass


@receiver(password_reset)
def notify_password_reset(request, user, **kwargs):
    pass


@receiver(password_set)
def notify_password_set(request, user, **kwargs):
    pass
