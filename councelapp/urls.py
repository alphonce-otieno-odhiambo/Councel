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
    path('group_view/',views.group_view,name='counsellor_groups'),
    path('get_counsellors/',views.get_counsellors,name='counsellors'),
    path('join_counsellor/',views.join_counsellor,name='join_counsellor'),
    path('ClientView/',views.ClientView,name="ClientView"),
    path('client_profile/',views.client_profile,name="client_profile"),
    path('counselling/',views.counselling,name="counselling"),
    path('conversation/',views.conversation,name="conversation"),
    path('messagess/',views.messagess,name="messagess"),
    path('api/', include(router.urls), name = 'api'),

]



