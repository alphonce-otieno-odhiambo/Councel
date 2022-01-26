from django.urls import path
from .views import *
from rest_framework import routers
from . import views

from django.urls import path, include,re_path


router = routers.DefaultRouter()
router.register('Appointment', views.AppointmentView),



urlpatterns = [

    path('appointments/', views.AppointmentsAPI.as_view()),
    
    re_path(r'^apointment/appointment-id/(?P<pk>[0-9]+)$', views.AppointmentAPI.as_view()),
    
    # path('addpres/',views.addpres,name='addpres'),
    # path('showpres/',views.showpres,name='showpres'),
    # path('showmedhis/',views.showmedhis,name='showmedhis'),



        

]