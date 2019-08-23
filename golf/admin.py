from django.contrib import admin

from . import models


class ProductInline(admin.TabularInline):
    model = models.Club.products.through
    extra = 1
    ordering = ('position',)


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('title', 'agency_type',
                    'phone', 'email', 'bank_account',
                    'cancellable_days', 'due_days', 'bookable_days', 'deposit')
    search_fields = ('title',)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('title', 'hole', 'cart_rental_required', 'cart_fee', 'caddie_fee', 'phone', 'email',)
    search_fields = ('title',)
    inlines = (ProductInline,)
    exclude = ('products',)


class ClubProductAdmin(admin.ModelAdmin):
    list_display = ('season', 'day_of_week', 'slot')


class ClubProductListMembershipAdmin(admin.ModelAdmin):
    pass


'''
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
'''

admin.site.register(models.Agency, AgencyAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.ClubProduct, ClubProductAdmin)
admin.site.register(models.ClubProductListMembership, ClubProductListMembershipAdmin)
