from django.urls import path

from . import views

app_name = 'golf'

urlpatterns = [
    # Agency
    path('agency/booking/',
         views.AgencyBookingListView.as_view(), name="agency-booking-list"),

    path('agency/booking/create',
         views.AgencyBookingCreateView.as_view(), name="agency-booking-create"),

    path('agency/booking/<uuid:uuid>/',
         views.AgencyBookingDetailView.as_view(), name='agency-booking-detail'),

    path('agency/booking/<uuid:uuid>/change',
         views.AgencyBookingChangeUpdateView.as_view(), name='agency-booking-change'),

    path('agency/booking/<uuid:uuid>/accept',
         views.AgencyBookingAcceptUpdateView.as_view(), name='agency-booking-accept'),

    path('agency/booking/<uuid:uuid>/revoke',
         views.AgencyBookingRevokeUpdateView.as_view(), name='agency-booking-revoke'),

    path('agency/booking/<uuid:uuid>/delete/',
         views.AgencyBookingDeleteView.as_view(), name='agency-booking-delete'),

    # Staff
    path('staff/booking/',
         views.StaffBookingListView.as_view(), name="staff-booking-list"),

    path('staff/booking/<uuid:uuid>/',
         views.StaffBookingDetailView.as_view(), name='staff-booking-detail'),

    path('staff/booking/<uuid:uuid>/accept',
         views.StaffBookingAcceptUpdateView.as_view(), name='staff-booking-accept'),

    path('staff/booking/<uuid:uuid>/confirm',
         views.StaffBookingConfirmUpdateView.as_view(), name='staff-booking-confirm'),

    path('staff/booking/<uuid:uuid>/offer',
         views.StaffBookingOfferUpdateView.as_view(), name='staff-booking-offer'),

    path('staff/booking/<uuid:uuid>/void',
         views.StaffBookingVoidUpdateView.as_view(), name='staff-booking-void'),

    # AJAX APIs
    path('api/fee/',
         views.APIFeeView.as_view(), name='api-fee'),

    path('api/tee-off-time/add/',
         views.APITeeOffTimeAddView.as_view(), name='api-tee-off-time-add'),

    path('api/tee-off-time/delete/',
         views.APITeeOffTimeDeleteView.as_view(), name='api-tee-off-time-delete'),

    path('api/tee-off-time/accept/',
         views.APITeeOffTimeAcceptView.as_view(), name='api-tee-off-time-accept'),
]
