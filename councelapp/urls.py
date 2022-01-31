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
    
    path('CounsellorView/', views.CounsellorView, name='CounsellorView'),
    path('join_counsellor/<int:id>', views.join_counsellor, name = 'join_counsellor'),  
    path('counsellor_profile/', views.counsellor_profile, name='counsellor_profile'),  
    
    path('api/', include(router.urls), name = 'api'),
    path("profile/",views.profile, name="profile"),
    path('group_view/',views.group_view,name='group_view'),
    path('get_counsellors/',views.get_counsellors,name='counsellors'),
    path('showmedhis/',views.showmedhis,name='showmedhis'),
    path('join_counsellor/<int:pk>',user_views.join_counsellor,name="join_counsellor")
    path('api/', include(router.urls), name = 'api'),
]




