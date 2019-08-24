from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class ProductInline(admin.TabularInline):
    model = models.Club.products.through
    extra = 1
    ordering = ('position',)


class ClubProductInline(admin.TabularInline):
    model = models.Agency.products.through
    extra = 1
    ordering = ('agency', 'position',)


class DepositInline(admin.TabularInline):
    model = models.Deposit
    extra = 1
    fields = ('amount', 'received')
    ordering = ('-created',)


class ProfileSetInline(admin.TabularInline):
    model = models.AgentProfile
    extra = 1
    fields = ('agency', 'cellphone', 'line_id')


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('holiday', 'country', 'title')
    list_filter = ('holiday', 'country')
    search_fields = ('title',)
    ordering = ('-holiday',)
    date_hierarchy = 'holiday'


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('title', 'agency_type',
                    'phone', 'email', 'bank_account',
                    'cancellable_days', 'due_days', 'bookable_days')
    search_fields = ('title',)
    inlines = (ClubProductInline, DepositInline,)


class ClubAdmin(admin.ModelAdmin):
    list_display = ('title', 'hole', 'cart_rental_required', 'cart_fee', 'caddie_fee', 'phone', 'email',)
    search_fields = ('title',)
    inlines = (ProductInline,)
    exclude = ('products',)


class ClubProductAdmin(admin.ModelAdmin):
    list_display = ('season', 'day_of_week', 'slot')
    ordering = ('season', 'day_of_week', 'slot')


class AgencyClubProductListMembershipAdmin(admin.ModelAdmin):
    list_display = ('agency_title', 'product_list', 'fee')
    list_filter = ('agency__title',)
    raw_id_fields = ('agency', 'product_list')

    def agency_title(self, obj):
        if obj.agency:
            return obj.agency.title
        else:
            return _('No organization')

    agency_title.short_description = _('Agency')
    agency_title.admin_order_field = 'agency__title'


class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency_title', 'cellphone', 'line_id')
    list_filter = ('agency__title',)
    list_select_related = ('agency',)
    search_fields = ('user__email', 'cellphone',)
    raw_id_fields = ('user', 'agency')
    ordering = ('-created',)

    fieldsets = (
        (_('Account'), {
            'fields': ('user',)
        }),
        (_('Profile'), {
            'fields': ('agency', 'cellphone', 'line_id')
        }),
    )

    def get_queryset(self, request):
        return super(AgentProfileAdmin, self) \
            .get_queryset(request) \
            .select_related('user', 'agency')

    def agency_title(self, obj):
        if obj.agency:
            return obj.agency.title
        else:
            return _('No organization')

    agency_title.short_description = _('Agency')
    agency_title.admin_order_field = 'agency__title'


class BookingAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Holiday, HolidayAdmin)
admin.site.register(models.Agency, AgencyAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.ClubProduct, ClubProductAdmin)
admin.site.register(models.AgentProfile, AgentProfileAdmin)
admin.site.register(models.AgencyClubProductListMembership, AgencyClubProductListMembershipAdmin)
admin.site.register(models.Booking, BookingAdmin)
