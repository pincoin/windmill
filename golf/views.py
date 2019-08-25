from django.contrib.auth import mixins as auth_mixins
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from . import models


class AgencyBookingList(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'golf/agency_booking_list.html'
    context_object_name = 'booking_list'

    def get_queryset(self):
        queryset = models.Booking.objects \
            .select_related('club', 'agency', 'agent') \
            .filter(agent__id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AgencyBookingList, self).get_context_data(**kwargs)
        context['page_title'] = _('Booking management')
        return context


class AgencyBookingCreate(auth_mixins.LoginRequiredMixin, generic.CreateView):
    pass


class AgencyBookingDetail(auth_mixins.LoginRequiredMixin, generic.DetailView):
    pass


class AgencyBookingDelete(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    pass


class StaffBookingList(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'golf/staff_booking_list.html'
    context_object_name = 'booking_list'

    def get_queryset(self):
        queryset = models.Booking.objects \
            .select_related('club', 'agency', 'agent')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StaffBookingList, self).get_context_data(**kwargs)
        context['page_title'] = _('Booking management')
        return context


class StaffBookingDetail(auth_mixins.LoginRequiredMixin, generic.DetailView):
    pass


class StaffBookingDelete(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    pass
