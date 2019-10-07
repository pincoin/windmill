from django.contrib import admin

from . import models


class PunchLogInline(admin.TabularInline):
    model = models.PunchLog
    extra = 1
    fields = ('status', 'punch_time', 'longitude', 'latitude')
    ordering = ('punch_time',)


class TimeSheetAdmin(admin.ModelAdmin):
    inlines = (PunchLogInline,)


admin.site.register(models.TimeSheet, TimeSheetAdmin)
