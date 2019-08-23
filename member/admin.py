from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from . import models


class LoginLogAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'ip_address', 'created'
    )
    list_select_related = ('user', 'user__agentprofile')
    readonly_fields = ('user', 'ip_address')
    search_fields = ('user__email', 'ip_address')
    ordering = ('-created',)

    def get_queryset(self, request):
        return super(LoginLogAdmin, self).get_queryset(request) \
            .select_related('user', 'user__agentprofile') \
            .filter(user__agentprofile__isnull=False)


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
            .select_related('user', 'user__agentprofile') \
            .filter(user__agentprofile__isnull=False)

    def get_edit_link(self, obj=None):
        if obj.user.agentprofile:  # if object has already been saved and has a primary key, show link to it
            # url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))
            return mark_safe('<a href="{url}">{text}</a>'.format(
                url=reverse('admin:golf_agentprofile_change', args=(obj.user.agentprofile.pk,)),
                text='{} {}'.format(obj.user.first_name, obj.user.last_name),
            ))
        return _("(save and continue editing to create a link)")

    get_edit_link.short_description = _('Agent profile')


admin.site.register(models.LoginLog, LoginLogAdmin)
admin.site.register(models.OrganizationApplication, OrganizationApplicationAdmin)
