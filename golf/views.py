import re

from django.http import (
    JsonResponse, HttpResponse
)
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import date as _date
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from . import forms
from . import models
from . import viewmixins
from .utils import get_fee


class AgencyBookingListView(viewmixins.PageableMixin, viewmixins.GroupRequiredMixin, generic.ListView):
    group_required = ['agency', ]
    template_name = 'golf/agency_booking_list.html'
    context_object_name = 'booking_list'

    booking_search_form_class = forms.BookingSearchForm
    booking_status_search_form_class = forms.BookingStatusSearchForm
    booking_club_search_form_class = forms.BookingGolfClubSearchForm
    booking_agency_search_form_class = forms.BookingAgencySearchForm

    def get_queryset(self):
        queryset = models.Booking.objects \
            .select_related('club', 'agency', 'agent__agentprofile') \
            .filter(agent__id=self.request.user.id)

        if 'status' in self.request.GET and self.request.GET['status']:
            queryset = queryset.filter(status=int(self.request.GET['status'].strip()))

        if 'club' in self.request.GET and self.request.GET['club']:
            queryset = queryset.filter(status=int(self.request.GET['club'].strip()))

        if 'category' in self.request.GET \
                and 'keyword' in self.request.GET \
                and self.request.GET['keyword']:

            print(self.request.GET['category'])
            print(self.request.GET['keyword'])
            if self.request.GET['category'] == '1':
                queryset = queryset.filter(fullname__contains=self.request.GET['keyword'].strip())
            elif self.request.GET['category'] == '2':
                queryset = queryset.filter(memo__contains=self.request.GET['keyword'].strip())

        return queryset.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(AgencyBookingListView, self).get_context_data(**kwargs)
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


class AgencyBookingCreateView(viewmixins.GroupRequiredMixin, generic.CreateView):
    group_required = ['agency', ]
    template_name = 'golf/agency_booking_create.html'
    form_class = forms.BookingForm

    def get_context_data(self, **kwargs):
        context = super(AgencyBookingCreateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Make an order')
        return context

    def get_form_kwargs(self):
        kwargs = super(AgencyBookingCreateView, self).get_form_kwargs()
        kwargs['club'] = 1
        return kwargs

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
        form.instance.season = fee['season_id']
        form.instance.day_of_week = fee['day_of_week_id']

        pattern = re.compile(r'^[가-힣]+$')  # Only Hangul

        if pattern.match(form.cleaned_data['last_name']) and pattern.match(form.cleaned_data['first_name']):
            form.instance.fullname = '{}{}'.format(form.cleaned_data['last_name'], form.cleaned_data['first_name'])
        else:
            form.instance.fullname = '{} {}'.format(form.cleaned_data['first_name'], form.cleaned_data['last_name'])

        return super(AgencyBookingCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super(AgencyBookingCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('golf:agency-booking-list')


class AgencyBookingDetailView(viewmixins.GroupRequiredMixin, generic.DetailView):
    group_required = ['agency', ]
    model = models.Booking
    context_object_name = 'booking'
    template_name = 'golf/agency_booking_detail.html'

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Booking.objects \
            .filter(agent=self.request.user) \
            .select_related('club', 'agency', 'agent__agentprofile')
        return get_object_or_404(queryset, booking_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(AgencyBookingDetailView, self).get_context_data(**kwargs)
        context['page_title'] = _('Booking Details')
        return context


class AgencyBookingChangeUpdateView(viewmixins.GroupRequiredMixin, generic.UpdateView):
    group_required = ['agency', ]
    model = models.Booking
    context_object_name = 'booking'
    template_name = 'golf/agency_booking_change_update.html'
    form_class = forms.BookingChangeForm

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Booking.objects \
            .filter(agent=self.request.user) \
            .select_related('club', 'agency', 'agent__agentprofile')
        return get_object_or_404(queryset, booking_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(AgencyBookingChangeUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Order waiting')
        return context

    def get_form_kwargs(self):
        kwargs = super(AgencyBookingChangeUpdateView, self).get_form_kwargs()
        kwargs['booking'] = self.object
        kwargs['club'] = self.object.club.id
        return kwargs

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
        form.instance.season = fee['season_id']
        form.instance.day_of_week = fee['day_of_week_id']

        pattern = re.compile(r'^[가-힣]+$')  # Only Hangul

        if pattern.match(form.cleaned_data['last_name']) and pattern.match(form.cleaned_data['first_name']):
            form.instance.fullname = '{}{}'.format(form.cleaned_data['last_name'], form.cleaned_data['first_name'])
        else:
            form.instance.fullname = '{} {}'.format(form.cleaned_data['first_name'], form.cleaned_data['last_name'])

        return super(AgencyBookingChangeUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('golf:agency-booking-change', args=(self.object.booking_uuid,))


class AgencyBookingAcceptUpdateView(viewmixins.GroupRequiredMixin, generic.UpdateView):
    group_required = ['agency', ]
    model = models.Booking
    context_object_name = 'booking'
    template_name = 'golf/agency_booking_accept_update.html'
    form_class = forms.BookingChangeForm

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Booking.objects \
            .filter(agent=self.request.user) \
            .select_related('club', 'agency', 'agent__agentprofile') \
            .prefetch_related('bookingteeofftime_set')
        return get_object_or_404(queryset, booking_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(AgencyBookingAcceptUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Accept/Reject tee-off time offer')
        return context

    def get_form_kwargs(self):
        kwargs = super(AgencyBookingAcceptUpdateView, self).get_form_kwargs()
        kwargs['booking'] = self.object
        kwargs['club'] = self.object.club.id
        return kwargs

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
        form.instance.season = fee['season_id']
        form.instance.day_of_week = fee['day_of_week_id']

        pattern = re.compile(r'^[가-힣]+$')  # Only Hangul

        if pattern.match(form.cleaned_data['last_name']) and pattern.match(form.cleaned_data['first_name']):
            form.instance.fullname = '{}{}'.format(form.cleaned_data['last_name'], form.cleaned_data['first_name'])
        else:
            form.instance.fullname = '{} {}'.format(form.cleaned_data['first_name'], form.cleaned_data['last_name'])

        return super(AgencyBookingAcceptUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('golf:agency-booking-change', args=(self.object.booking_uuid,))


class AgencyBookingRevokeUpdateView(viewmixins.GroupRequiredMixin, generic.UpdateView):
    group_required = ['agency', ]
    model = models.Booking
    context_object_name = 'booking'
    template_name = 'golf/agency_booking_revoke_update.html'
    form_class = forms.BookingDummyForm

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Booking.objects \
            .filter(status__in=[models.Booking.STATUS_CHOICES.payment_pending, models.Booking.STATUS_CHOICES.offered]) \
            .select_related('club', 'agency', 'agent__agentprofile')
        return get_object_or_404(queryset, booking_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(AgencyBookingRevokeUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Change order')
        return context

    def form_valid(self, form):
        form.instance.status = models.Booking.STATUS_CHOICES.order_made
        return super(AgencyBookingRevokeUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('golf:agency-booking-change', args=(self.object.booking_uuid,))


class AgencyBookingDeleteView(viewmixins.GroupRequiredMixin, generic.DeleteView):
    group_required = ['agency', ]
    model = models.Booking
    context_object_name = 'booking'
    template_name = 'golf/agency_booking_confirm_delete.html'

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Booking.objects \
            .filter(agent=self.request.user,
                    status__in=[
                        models.Booking.STATUS_CHOICES.order_made,
                        models.Booking.STATUS_CHOICES.voided,
                        models.Booking.STATUS_CHOICES.offered,
                    ]) \
            .select_related('club', 'agency', 'agent__agentprofile')
        return get_object_or_404(queryset, booking_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(AgencyBookingDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = _('Delete booking')
        return context

    def get_success_url(self):
        return reverse('golf:agency-booking-list')


class StaffBookingListView(viewmixins.PageableMixin, viewmixins.GroupRequiredMixin, generic.ListView):
    group_required = ['staff', ]
    template_name = 'golf/staff_booking_list.html'
    context_object_name = 'booking_list'

    booking_search_form_class = forms.BookingSearchForm
    booking_status_search_form_class = forms.BookingStatusSearchForm
    booking_club_search_form_class = forms.BookingGolfClubSearchForm
    booking_agency_search_form_class = forms.BookingAgencySearchForm

    def get_queryset(self):
        queryset = models.Booking.objects \
            .select_related('club', 'agency', 'agent__agentprofile')

        if 'status' in self.request.GET and self.request.GET['status']:
            queryset = queryset.filter(status=int(self.request.GET['status'].strip()))

        if 'club' in self.request.GET and self.request.GET['club']:
            queryset = queryset.filter(status=int(self.request.GET['club'].strip()))

        if 'category' in self.request.GET \
                and 'keyword' in self.request.GET \
                and self.request.GET['keyword']:

            print(self.request.GET['category'])
            print(self.request.GET['keyword'])
            if self.request.GET['category'] == '1':
                queryset = queryset.filter(fullname__contains=self.request.GET['keyword'].strip())
            elif self.request.GET['category'] == '2':
                queryset = queryset.filter(memo__contains=self.request.GET['keyword'].strip())

        return queryset.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(StaffBookingListView, self).get_context_data(**kwargs)
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


class StaffBookingDetailView(viewmixins.GroupRequiredMixin, generic.DetailView):
    group_required = ['staff', ]
    model = models.Booking
    context_object_name = 'booking'
    template_name = 'golf/staff_booking_detail.html'

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Booking.objects \
            .select_related('club', 'agency', 'agent__agentprofile')
        return get_object_or_404(queryset, booking_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(StaffBookingDetailView, self).get_context_data(**kwargs)
        context['page_title'] = _('Booking Details')
        return context


class StaffBookingAcceptUpdateView(viewmixins.GroupRequiredMixin, generic.UpdateView):
    group_required = ['staff', ]
    model = models.Booking
    context_object_name = 'booking'
    template_name = 'golf/staff_booking_accept_update.html'
    form_class = forms.BookingDummyForm

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Booking.objects \
            .filter(status=models.Booking.STATUS_CHOICES.order_made) \
            .select_related('club', 'agency', 'agent__agentprofile')
        return get_object_or_404(queryset, booking_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(StaffBookingAcceptUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Accept order')
        return context

    def form_valid(self, form):
        form.instance.status = models.Booking.STATUS_CHOICES.order_pending
        return super(StaffBookingAcceptUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('golf:staff-booking-confirm', args=(self.object.booking_uuid,))


class StaffBookingConfirmUpdateView(viewmixins.GroupRequiredMixin, generic.UpdateView):
    group_required = ['staff', ]
    model = models.Booking
    context_object_name = 'booking'
    template_name = 'golf/staff_booking_confirm_update.html'
    form_class = forms.BookingConfirmForm
    tee_off_time_add_form_class = forms.TeeOffTimeAddForm

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Booking.objects \
            .filter(status=models.Booking.STATUS_CHOICES.order_pending) \
            .select_related('club', 'agency', 'agent__agentprofile') \
            .prefetch_related('bookingteeofftime_set')
        return get_object_or_404(queryset, booking_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(StaffBookingConfirmUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Confirm order')
        context['tee_off_time_add_form'] = self.tee_off_time_add_form_class(booking=self.object)
        return context

    def get_form_kwargs(self):
        kwargs = super(StaffBookingConfirmUpdateView, self).get_form_kwargs()
        kwargs['booking'] = self.object
        return kwargs

    def form_valid(self, form):
        form.instance.status = models.Booking.STATUS_CHOICES.payment_pending

        form.instance.tee_off_time = timezone.datetime.strptime('{}:{}:00'.format(
            form.cleaned_data['tee_off_time_hour'],
            form.cleaned_data['tee_off_time_minute']), '%H:%M:%S').time()

        return super(StaffBookingConfirmUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('golf:staff-booking-detail', args=(self.object.booking_uuid,))


class StaffBookingOfferUpdateView(viewmixins.GroupRequiredMixin, generic.UpdateView):
    group_required = ['staff', ]
    model = models.Booking
    context_object_name = 'booking'
    template_name = 'golf/staff_booking_confirm_update.html'
    form_class = forms.BookingDummyForm

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Booking.objects \
            .filter(status=models.Booking.STATUS_CHOICES.order_pending) \
            .select_related('club', 'agency', 'agent__agentprofile')
        return get_object_or_404(queryset, booking_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(StaffBookingOfferUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Offer tee-off time')
        return context

    def form_valid(self, form):
        form.instance.status = models.Booking.STATUS_CHOICES.offered
        return super(StaffBookingOfferUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('golf:staff-booking-detail', args=(self.object.booking_uuid,))


class StaffBookingVoidUpdateView(viewmixins.GroupRequiredMixin, generic.UpdateView):
    group_required = ['staff', ]
    model = models.Booking
    context_object_name = 'booking'
    template_name = 'golf/staff_booking_void_update.html'
    form_class = forms.BookingDummyForm

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Booking.objects \
            .filter(status=models.Booking.STATUS_CHOICES.order_pending) \
            .select_related('club', 'agency', 'agent__agentprofile')
        return get_object_or_404(queryset, booking_uuid=self.kwargs['uuid'])

    def get_context_data(self, **kwargs):
        context = super(StaffBookingVoidUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = _('Void order')
        return context

    def form_valid(self, form):
        form.instance.status = models.Booking.STATUS_CHOICES.voided
        return super(StaffBookingVoidUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('golf:staff-booking-list')


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


class APITeeOffTimeAddView(viewmixins.GroupRequiredMixin, generic.FormView):
    group_required = ['staff', ]
    form_class = forms.TeeOffTimeAPIAddForm

    def form_valid(self, form):
        data = form.cleaned_data

        tee_off_time = timezone.datetime.strptime('{}:{}:00'.format(
            form.cleaned_data['offer_tee_off_time_hour'],
            form.cleaned_data['offer_tee_off_time_minute']), '%H:%M:%S').time()

        try:
            booking = models.Booking.objects.get(booking_uuid=form.cleaned_data['booking_uuid'])

            t = models.BookingTeeOffTime()
            t.booking = booking
            t.tee_off_time = tee_off_time
            t.status = models.BookingTeeOffTime.STATUS_CHOICES.offered
            t.save()

            data.update({
                'tee_off_time': tee_off_time,
                'tee_off_time_str': _date(tee_off_time, 'H:i'),
            })
        except:
            pass

        return JsonResponse(data)

    def form_invalid(self, form):
        return HttpResponse(form.errors.as_json(), status=400, content_type='application/json')


class APITeeOffTimeDeleteView(viewmixins.GroupRequiredMixin, generic.FormView):
    group_required = ['staff', ]
    form_class = forms.TeeOffTimeDeleteForm

    def form_valid(self, form):
        data = form.cleaned_data

        try:
            t = models.BookingTeeOffTime.objects \
                .exclude(status__in=[models.BookingTeeOffTime.STATUS_CHOICES.accepted]) \
                .get(pk=form.cleaned_data['tee_off_time_pk'])

            t.delete()
        except models.BookingTeeOffTime.DoesNotExist:
            pass

        return JsonResponse(data)

    def form_invalid(self, form):
        return HttpResponse(form.errors.as_json(), status=400, content_type='application/json')


class APITeeOffTimeAcceptView(viewmixins.GroupRequiredMixin, generic.FormView):
    group_required = ['agency', ]
    form_class = forms.TeeOffTimeAcceptForm

    def form_valid(self, form):
        data = form.cleaned_data

        try:
            t = models.BookingTeeOffTime.objects \
                .filter(status=models.BookingTeeOffTime.STATUS_CHOICES.offered) \
                .get(pk=form.cleaned_data['tee_off_time_pk'])

            t.booking.bookingteeofftime_set.all().update(status=models.BookingTeeOffTime.STATUS_CHOICES.offered)

            t.status = models.BookingTeeOffTime.STATUS_CHOICES.accepted
            t.save()

            data.update({
                'tee_off_time_pk': t.pk,
            })
        except models.BookingTeeOffTime.DoesNotExist:
            pass

        return JsonResponse(data)

    def form_invalid(self, form):
        return HttpResponse(form.errors.as_json(), status=400, content_type='application/json')
