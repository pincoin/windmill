from django import template

from .. import models

register = template.Library()


@register.simple_tag
def get_tee_off_time_list(booking_uuid):
    return models.BookingTeeOffTime.objects \
        .filter(booking__booking_uuid=booking_uuid)
