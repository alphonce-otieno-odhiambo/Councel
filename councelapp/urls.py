from django.urls import path , include
from . import views

from . import views 
from rest_framework import routers
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView

router = routers.DefaultRouter()
router.register('Councelorprofile', views.CounselorProfView),
router.register('Councelor', views.CounselorView),
router.register('Appointment', views.AppointmentView),
router.register('Appointment', views.PrescriptView),
router.register('GroupView', views.GroupView),
router.register('ClientProfileView', views.ClientProfileView),



urlpatterns = [
    
    path('counselprofile/', views.counselprofile, name='counselprofile'),
    path('update_profile/<int:id>', views.update_profile, name = 'update_profile'),  
    path('counselor/', views.counselor, name='counselor'),  
    
    path('api/', include(router.urls), name = 'api'),
    path("",views.HomeTemplateView, name="home"),
    #path("make-an-appointment/", AppointmentTemplateView.as_view(), name="appointment"),
    #path("manage-appointments/", ManageAppointmentTemplateView.as_view(), name="manage"),
    path('addpres/',views.addpres,name='addpres'),
    path('showpres/',views.showpres,name='showpres'),
    path('showmedhis/',views.showmedhis,name='showmedhis'),
    path('api/', include(router.urls), name = 'api'),
]




