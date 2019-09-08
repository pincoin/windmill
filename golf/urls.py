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

    path('agency/booking/<uuid:uuid>/update',
         views.AgencyBookingUpdateView.as_view(), name='agency-booking-update'),

    path('agency/booking/<uuid:uuid>/delete/',
         views.AgencyBookingDeleteView.as_view(), name='agency-booking-delete'),

    # Staff
    path('staff/booking/',
         views.StaffBookingListView.as_view(), name="staff-booking-list"),

    path('staff/booking/<uuid:uuid>/',
         views.StaffBookingDetailView.as_view(), name='staff-booking-detail'),

    path('staff/booking/<uuid:uuid>/accept',
         views.AgencyBookingAcceptUpdateView.as_view(), name='staff-booking-accept'),

    path('staff/booking/<uuid:uuid>/update/',
         views.StaffBookingDetailView.as_view(), name='staff-booking-update'),

    # AJAX APIs
    path('api/fee/',
         views.APIFeeView.as_view(), name='api-fee'),
]
