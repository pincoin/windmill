from django.contrib import admin

from . import models


class ProfileAdmin(admin.ModelAdmin):
    pass


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
