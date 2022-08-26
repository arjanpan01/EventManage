from django.urls import path
from . import views

urlpatterns = [
    path('', views.initialTable, name='initialTable'),
    path('newevent', views.newEvent, name='newEvent'),
    path('updateevent/<eventID>', views.updateEvent, name="updateEvent"),
    path('dashboard/<eventID>', views.goToDashboard, name="dashboardView"),
    path('attendee/<attendeeID>/<eventID>', views.goToAttendees, name="attendeeView"),
    path('changedate/<attendeeID>/<eventID>/<dateID>', views.changeDate, name="changeDate"),
    path('updateattendance/<attendeeID>/<eventID>/', views.updateAttendance, name="updateAttendance"),
    path('updateaccomplice/<attendeeID>/<eventID>/<accompliceID>', views.updateAccomplice, name="updateAccomplice"),
    path('addstage/<attendeeID>/<eventID>', views.addStage, name="addStage"),
]