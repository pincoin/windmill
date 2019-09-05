from django.utils import timezone

from . import models


def get_fee(club_id, agency_id, round_date, slot):
    club = models.Club.objects.get(pk=club_id)

    round_date = timezone.make_aware(timezone.datetime.strptime(round_date, '%Y-%m-%d'))

    if round_date.weekday() in [5, 6]:
        day_of_week = models.Booking.DAY_CHOICES.weekend
    else:
        day_of_week = models.Booking.DAY_CHOICES.weekday

    if models.Holiday.objects \
            .filter(holiday=round_date.date(), country=models.Holiday.COUNTRY_CHOICES.thailand) \
            .exists():
        day_of_week = models.Booking.DAY_CHOICES.weekend

    if 1 << round_date.month - 1 & club.high_season:
        season = models.Booking.SEASON_CHOICES.high
    else:
        season = models.Booking.SEASON_CHOICES.low

    queryset = models.AgencyClubProductListMembership.objects \
        .select_related('product_list__product_list', 'product_list__club', 'agency') \
        .filter(agency=agency_id,
                product_list__club=club_id,
                product_list__product_list__season=season,
                product_list__product_list__day_of_week=day_of_week,
                product_list__product_list__slot=slot)

    return {
        'season': models.Booking.SEASON_CHOICES[season],
        'day_of_week': models.Booking.DAY_CHOICES[day_of_week],
        'fee': queryset[0].fee,
    }
