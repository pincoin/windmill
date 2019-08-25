from django.contrib.auth import mixins as auth_mixins
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


class AgencyBookingCreate(auth_mixins.LoginRequiredMixin, generic.CreateView):
    pass


class AgencyBookingDetail(auth_mixins.LoginRequiredMixin, generic.DetailView):
    pass


class AgencyBookingDelete(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    pass


class StaffBookingList(auth_mixins.LoginRequiredMixin, generic.ListView):
    pass


class StaffBookingDetail(auth_mixins.LoginRequiredMixin, generic.DetailView):
    pass


class StaffBookingDelete(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    pass
