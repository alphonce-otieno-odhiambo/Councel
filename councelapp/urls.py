from django.urls import path , include
from . import views

from . import views as main_views
from rest_framework import routers
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView

router = routers.DefaultRouter()
router.register('Councelorprofile', views.CounselorProfileView),
router.register('Councelor', views.CounselorView),
router.register('Appointment', views.AppointmentView),


urlpatterns = [
    
    path('counselprofile/', views.counselprofile, name='counselprofile'),
    path('update_profile/<int:id>', views.update_profile, name = 'update_profile'),  
    path('counselor/', views.counselor, name='counselor'),  
    
    path('api/', include(router.urls), name = 'api'),
    path("", HomeTemplateView.as_view(), name="home"),
    path("make-an-appointment/", AppointmentTemplateView.as_view(), name="appointment"),
    path("manage-appointments/", ManageAppointmentTemplateView.as_view(), name="manage"),

    path('api/', include(router.urls), name = 'api'),
]




