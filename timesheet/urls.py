from django.urls import path

from . import views

app_name = 'timesheet'

urlpatterns = [
    path('list/',
         views.TimeSheetListView.as_view(), name="timesheet-list"),
    path('punch-in/',
         views.PunchInCreateView.as_view(), name="timesheet-punch-in"),
    path('punch-out/',
         views.PunchOutUpdateView.as_view(), name="timesheet-punch-out"),
]
