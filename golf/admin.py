from django.contrib import admin

from . import models


class TravelAgentAdmin(admin.ModelAdmin):
    pass


class GolfClubAdmin(admin.ModelAdmin):
    pass


class PriceTableAdmin(admin.ModelAdmin):
    list_filter = ('company__title', 'club__title')


admin.site.register(models.TravelAgent, TravelAgentAdmin)
admin.site.register(models.GolfClub, GolfClubAdmin)
admin.site.register(models.PriceTable, PriceTableAdmin)
