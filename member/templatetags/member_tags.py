from django import template
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.core.cache import cache
from geoip2.errors import AddressNotFoundError

from .. import models

register = template.Library()


@register.simple_tag
def groups(user):
    cache_key = 'member.member_tags.groups({})'.format(user.id)
    cache_time = settings.CACHES['default']['TIMEOUT']

    group_list = cache.get(cache_key)

    if not group_list:
        group_list = list(user.groups.all().values_list('name', flat=True))

        cache.set(cache_key, group_list, cache_time)

    return group_list


@register.simple_tag
def get_login_logs(user, count):
    cache_key = 'member.member_tags.get_login_logs({})'.format(user.id)
    cache_time = settings.CACHES['default']['TIMEOUT']

    logs = cache.get(cache_key)

    if not logs:
        logs = models.LoginLog.objects.filter(user=user).order_by('-created')[:count]

        for log in logs:
            log.country_code = None
            try:
                if log.ip_address not in ['127.0.0.1']:
                    country = GeoIP2().country(log.ip_address)
                    log.country_code = country['country_code'].lower()
            except AddressNotFoundError:
                pass

        cache.set(cache_key, logs, cache_time)

    return logs


@register.simple_tag
def get_organization_applications(user):
    return models.OrganizationApplication.objects.filter(user=user).order_by('-created')
