from decimal import Decimal

from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from ipware.ip import get_ip

from golf import viewmixins
from . import forms
from . import models


class TimeSheetListView(viewmixins.PageableMixin, viewmixins.GroupRequiredMixin, generic.ListView):
    group_required = ['staff', ]
    template_name = 'timesheet/timesheet_list.html'
    context_object_name = 'time_list'

    def get_queryset(self):
        queryset = models.TimeSheet.objects.filter(staff__id=self.request.user.id)

        return queryset.order_by('-punch_in_time')

    def get_context_data(self, **kwargs):
        context = super(TimeSheetListView, self).get_context_data(**kwargs)
        context['page_title'] = _('Time sheet')

        return context


class PunchInCreateView(viewmixins.GroupRequiredMixin, generic.CreateView):
    group_required = ['agency', ]
    template_name = 'timesheet/timesheet_create.html'
    form_class = forms.PunchLogForm

    def get_context_data(self, **kwargs):
        context = super(PunchInCreateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Punch-in')
        return context

    def form_valid(self, form):
        sheet = models.TimeSheet()
        sheet.staff = self.request.user
        sheet.save()

        form.instance.sheet = sheet
        form.instance.status = models.PunchLog.STATUS_CHOICES.punch_in

        form.instance.punch_time = timezone.make_aware(timezone.localtime().now())

        form.instance.punch_latitude = Decimal('3.14')
        form.instance.punch_longitude = Decimal('3.14')

        form.instance.user_agent = self.request.META['HTTP_USER_AGENT']
        form.instance.ip_address = get_ip(self.request)

        return super(PunchInCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(PunchInCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('timesheet:timesheet-list')


class PunchOutUpdateView(generic.TemplateView):
    template_name = 'timesheet/timesheet_detail.html'
