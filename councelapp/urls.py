from django.urls import path
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView
from rest_framework import routers
from . import views

from django.urls import path, include


router = routers.DefaultRouter()
router.register('Appointment', views.AppointmentView),



urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("make-an-appointment/", AppointmentTemplateView.as_view(), name="appointment"),
    path("manage-appointments/", ManageAppointmentTemplateView.as_view(), name="manage"),

    path('api/', include(router.urls), name = 'api'),


]