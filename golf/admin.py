from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('title', 'agency_type',
                    'phone', 'email', 'bank_account',
                    'cancellable_days', 'due_days', 'bookable_days', 'deposit')
    search_fields = ('title',)


class GolfClubAdmin(admin.ModelAdmin):
    list_display = ('title', 'hole', 'cart_rental_required', 'cart_fee', 'caddie_fee', 'phone', 'email',)
    search_fields = ('title',)


class GolfClubProductAdmin(admin.ModelAdmin):
    list_display = ('season', 'day_of_week', 'slot', 'time_start', 'time_end')


class PriceTableAdmin(admin.ModelAdmin):
    list_display = ('agency_title', 'club_title', 'season', 'day_of_week', 'slot', 'fee', 'cost', 'profit')
    search_fields = ('agency__title', 'club__title')
    list_filter = ('agency__title', 'club__title')
    raw_id_fields = ('agency', 'club')

    def get_queryset(self, request):
        return super(PriceTableAdmin, self) \
            .get_queryset(request) \
            .select_related('agency', 'club')

    def agency_title(self, obj):
        return obj.agency.title

    agency_title.short_description = _('Agency')
    agency_title.admin_order_field = 'agency__title'

    def club_title(self, obj):
        return obj.club.title

    club_title.short_description = _('Golf club')
    club_title.admin_order_field = 'club__title'


admin.site.register(models.Agency, AgencyAdmin)
admin.site.register(models.GolfClub, GolfClubAdmin)
admin.site.register(models.PriceTable, PriceTableAdmin)
admin.site.register(models.GolfClubProduct, GolfClubProductAdmin)
