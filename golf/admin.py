from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


class TravelAgentAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'email', 'website', 'deposit', 'bank_account')
    search_fields = ('title',)


class GolfClubAdmin(admin.ModelAdmin):
    list_display = ('title', 'hole', 'cart_rental_required', 'cart_fee', 'caddie_fee', 'phone', 'email',)
    search_fields = ('title',)


class PriceTableAdmin(admin.ModelAdmin):
    list_display = ('company_title', 'club_title', 'season', 'day_of_week', 'slot', 'fee', 'cost', 'profit')
    search_fields = ('company__title', 'club__title')
    list_filter = ('company__title', 'club__title')
    raw_id_fields = ('company', 'club')

    def get_queryset(self, request):
        return super(PriceTableAdmin, self) \
            .get_queryset(request) \
            .select_related('company', 'club')

    def company_title(self, obj):
        return obj.company.title

    company_title.short_description = _('Travel agent')
    company_title.admin_order_field = 'company__title'

    def club_title(self, obj):
        return obj.club.title

    club_title.short_description = _('Golf club')
    club_title.admin_order_field = 'club__title'


admin.site.register(models.TravelAgent, TravelAgentAdmin)
admin.site.register(models.GolfClub, GolfClubAdmin)
admin.site.register(models.PriceTable, PriceTableAdmin)
