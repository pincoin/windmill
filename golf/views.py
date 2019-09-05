from django.contrib.auth import mixins as auth_mixins
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from . import forms
from . import models


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
        print(form.cleaned_data)

        form.instance.agency = models.AgentProfile.objects \
            .select_related('agency') \
            .get(user__id=self.request.user.id) \
            .agency
        form.instance.agent = self.request.user
        form.instance.round_time = timezone.now()
        form.instance.fee = 3000

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

        club = models.Club.objects.get(pk=data['club_id'])

        round_date = timezone.make_aware(timezone.datetime.strptime(data['round_date'], '%Y-%m-%d'))

        if round_date.weekday() in [5, 6]:
            day_of_week = models.Booking.DAY_CHOICES.weekend
        else:
            day_of_week = models.Booking.DAY_CHOICES.weekday

        if models.Holiday.objects \
                .filter(holiday=round_date.date(), country=models.Holiday.COUNTRY_CHOICES.thailand) \
                .exists():
            day_of_week = models.Booking.DAY_CHOICES.weekend

        if 1 << round_date.month - 1 & club.high_season:
            season = models.Booking.SEASON_CHOICES.high
        else:
            season = models.Booking.SEASON_CHOICES.low

        queryset = models.AgencyClubProductListMembership.objects \
            .select_related('product_list__product_list', 'product_list__club', 'agency') \
            .filter(agency=data['agency_id'],
                    product_list__club=data['club_id'],
                    product_list__product_list__season=season,
                    product_list__product_list__day_of_week=day_of_week,
                    product_list__product_list__slot=data['slot'])

        data['season'] = models.Booking.SEASON_CHOICES[season]
        data['day_of_week'] = models.Booking.DAY_CHOICES[day_of_week]
        data['fee'] = queryset[0].fee

        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse(form.errors.as_json(), status=400)
