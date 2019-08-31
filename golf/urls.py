from django.urls import path

from . import views

app_name = 'golf'

urlpatterns = [
    # Agency
    path('agency/booking/',
         views.AgencyBookingList.as_view(), name="agency-booking-list"),

    path('agency/booking/create',
         views.AgencyBookingCreate.as_view(), name="agency-booking-create"),

    path('agency/booking/<uuid:uuid>/',
         views.AgencyBookingDetail.as_view(), name='agency-booking-detail'),

    path('agency/booking/<uuid:uuid>/delete/',
         views.AgencyBookingDelete.as_view(), name='agency-booking-delete'),

    # Staff
    path('staff/booking/',
         views.StaffBookingList.as_view(), name="staff-booking-list"),

    path('staff/booking/<uuid:uuid>/',
         views.StaffBookingDetail.as_view(), name='staff-booking-detail'),

    path('staff/booking/<uuid:uuid>/delete/',
         views.StaffBookingDelete.as_view(), name='staff-booking-delete'),

    # AJAX APIs
    path('api/fee/',
         views.APIFeeView.as_view(), name='api-fee'),
]
