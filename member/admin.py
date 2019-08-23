from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from . import models


class ProfileSetInline(admin.TabularInline):
    model = models.Profile
    extra = 1
    fields = ('agency', 'cellphone', 'line_id')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency_title', 'cellphone', 'line_id')
    list_filter = ('agency__title',)
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
        return super(ProfileAdmin, self) \
            .get_queryset(request) \
            .select_related('user', 'agency')

    def agency_title(self, obj):
        if obj.agency:
            return obj.agency.title
        else:
            return _('No organization')

    agency_title.short_description = _('Agency')
    agency_title.admin_order_field = 'agency__title'


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


class OrganizationApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'status', 'created'
    )

    fields = ('user', 'get_edit_link', 'message', 'status', 'created')
    readonly_fields = ('user', 'get_edit_link', 'message', 'created')

    raw_id_fields = ('user',)

    ordering = ('-created',)

    def get_queryset(self, request):
        return super(OrganizationApplicationAdmin, self).get_queryset(request) \
            .select_related('user', 'user__profile') \
            .filter(user__profile__isnull=False)

    def get_edit_link(self, obj=None):
        if obj.user.profile:  # if object has already been saved and has a primary key, show link to it
            # url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))
            return mark_safe('<a href="{url}">{text}</a>'.format(
                url=reverse('admin:member_profile_change', args=(obj.user.profile.pk,)),
                text='{} {}'.format(obj.user.first_name, obj.user.last_name),
            ))
        return _("(save and continue editing to create a link)")

    get_edit_link.short_description = _('Profile')


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.LoginLog, LoginLogAdmin)
admin.site.register(models.OrganizationApplication, OrganizationApplicationAdmin)
