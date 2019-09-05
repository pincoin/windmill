from django.contrib.auth import mixins as auth_mixins
from django.http import (
    JsonResponse, HttpResponse
)
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from . import forms
from . import models
from .utils import get_fee


class AgencyBookingList(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'golf/agency_booking_list.html'
    context_object_name = 'booking_list'

    booking_search_form_class = forms.BookingSearchForm
    booking_status_search_form_class = forms.BookingStatusSearchForm
    booking_club_search_form_class = forms.BookingGolfClubSearchForm
    booking_agency_search_form_class = forms.BookingAgencySearchForm

    def get_queryset(self):
        queryset = models.Booking.objects \
            .select_related('club', 'agency', 'agent') \
            .filter(agent__id=self.request.user.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AgencyBookingList, self).get_context_data(**kwargs)
        context['page_title'] = _('Booking management')

        context['booking_search_form'] = self.booking_search_form_class(
            category=self.request.GET.get('category') if self.request.GET.get('category') else '1',
            keyword=self.request.GET.get('keyword') if self.request.GET.get('keyword') else '',
        )

        context['booking_status_search_form'] = self.booking_status_search_form_class(
            status=self.request.GET.get('status') if self.request.GET.get('status') else '',
        )

        context['booking_club_search_form'] = self.booking_club_search_form_class(
            club=self.request.GET.get('club') if self.request.GET.get('club') else '',
        )

        context['booking_agency_search_form'] = self.booking_agency_search_form_class(
            agency=self.request.GET.get('agency') if self.request.GET.get('agency') else '',
        )

        return context


class AgencyBookingCreate(auth_mixins.LoginRequiredMixin, generic.CreateView):
    template_name = 'golf/agency_booking_create.html'
    form_class = forms.BookingForm

    def get_context_data(self, **kwargs):
        context = super(AgencyBookingCreate, self).get_context_data(**kwargs)
        context['page_title'] = _('Make an order')
        return context

    def form_valid(self, form):
        form.instance.agency = models.AgentProfile.objects \
            .select_related('agency') \
            .get(user__id=self.request.user.id) \
            .agency

        form.instance.agent = self.request.user

        form.instance.round_time = timezone.datetime.strptime('{}:{}:00'.format(
            form.cleaned_data['round_time_hour'],
            form.cleaned_data['round_time_minute']), '%H:%M:%S').time()

        fee = get_fee(form.cleaned_data['club'].id,
                      form.instance.agency.id,
                      form.cleaned_data['round_date'],
                      form.cleaned_data['slot'])

        form.instance.fee = fee['fee'] * int(form.cleaned_data['people'])

        return super(AgencyBookingCreate, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(AgencyBookingCreate, self).form_invalid(form)

    def get_success_url(self):
        return reverse('golf:agency-booking-list')


class AgencyBookingDetail(auth_mixins.LoginRequiredMixin, generic.DetailView):
    pass


class AgencyBookingDelete(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    pass


class StaffBookingList(auth_mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'golf/staff_booking_list.html'
    context_object_name = 'booking_list'

    booking_search_form_class = forms.BookingSearchForm
    booking_status_search_form_class = forms.BookingStatusSearchForm
    booking_club_search_form_class = forms.BookingGolfClubSearchForm
    booking_agency_search_form_class = forms.BookingAgencySearchForm

    def get_queryset(self):
        queryset = models.Booking.objects \
            .select_related('club', 'agency', 'agent')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StaffBookingList, self).get_context_data(**kwargs)
        context['page_title'] = _('Booking management')

        context['booking_search_form'] = self.booking_search_form_class(
            category=self.request.GET.get('category') if self.request.GET.get('category') else '1',
            keyword=self.request.GET.get('keyword') if self.request.GET.get('keyword') else '',
        )

        context['booking_status_search_form'] = self.booking_status_search_form_class(
            status=self.request.GET.get('status') if self.request.GET.get('status') else '',
        )

        context['booking_club_search_form'] = self.booking_club_search_form_class(
            club=self.request.GET.get('club') if self.request.GET.get('club') else '',
        )

        context['booking_agency_search_form'] = self.booking_agency_search_form_class(
            agency=self.request.GET.get('agency') if self.request.GET.get('agency') else '',
        )

        return context


class StaffBookingDetail(auth_mixins.LoginRequiredMixin, generic.DetailView):
    pass


class StaffBookingDelete(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    pass


class APIFeeView(generic.FormView):
    form_class = forms.FeeForm

    def form_valid(self, form):
        data = form.cleaned_data

        data.update(get_fee(form.cleaned_data['club_id'],
                            form.cleaned_data['agency_id'],
                            form.cleaned_data['round_date'],
                            form.cleaned_data['slot']))

        return JsonResponse(data)

    def form_invalid(self, form):
        return HttpResponse(form.errors.as_json(), status=400, content_type='application/json')
