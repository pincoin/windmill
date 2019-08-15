from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from . import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cellphone', 'line_id', 'company')
    list_filter = ('company__title',)
    search_fields = ('user__email', 'cellphone',)
    raw_id_fields = ('user',)
    ordering = ('-created',)

    fieldsets = (
        (_('Account'), {
            'fields': ('user',)
        }),
        (_('Profile'), {
            'fields': ('cellphone', 'line_id', 'company')
        }),
    )

    def get_queryset(self, request):
        return super(ProfileAdmin, self) \
            .get_queryset(request) \
            .select_related('user')


class LoginLogAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'ip_address', 'created'
    )
    list_select_related = ('user', 'user__profile')
    readonly_fields = ('user', 'ip_address')
    search_fields = ('user__email', 'ip_address')
    ordering = ('-created',)

    def get_queryset(self, request):
        return super(LoginLogAdmin, self).get_queryset(request) \
            .select_related('user', 'user__profile') \
            .filter(user__profile__isnull=False)


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.LoginLog, LoginLogAdmin)
