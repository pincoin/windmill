from django.views import generic


class AgencyBookingList(generic.ListView):
    pass


class AgencyBookingCreate(generic.CreateView):
    pass


class AgencyBookingDetail(generic.DetailView):
    pass


class AgencyBookingDelete(generic.DeleteView):
    pass


class StaffBookingList(generic.ListView):
    pass


class StaffBookingDetail(generic.DetailView):
    pass


class StaffBookingDelete(generic.DeleteView):
    pass
