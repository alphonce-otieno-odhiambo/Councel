from unicodedata import name
from urllib.parse import uses_relative
from django.urls import path
from councelapp import views as user_views
from rest_framework.authtoken import views
from rest_framework.authtoken import views as special_views

from .views import *

urlpatterns = [
    path('counsellor_details',user_views.CounsellorView,name='counsellor'),
    path('current_date',user_views.current_date,name="date"),
    path('counsellors',user_views.get_counsellors,name="counsellors"),
    path('get_counsellor',user_views.clients_counsellor,name="get_counsellor"),
    path('join_counsellor/<int:pk>',user_views.join_counsellor,name='join_counsellor'),
    path('counsellor_profile',user_views.counsellor_profile,name='profile'),
    path('client_profile',user_views.profile,name="client_profile"),
    path('my_clients/<int:pk>',user_views.get_clients,name='get_clients'),
    path('client_group',user_views.get_group,name='get_group'),
    path('join_group/<int:pk>',user_views.join_group,name="join_group"),
    path('group_view',user_views.group_view,name='counsellor_groups'),
    path('messages',MessageAPIView.as_view()),
    path('group_chat/<int:pk>',user_views.group_chat,name="group_chat"),
    path('join_counsellor/<int:pk>',user_views.join_counsellor,name="join_counsellor"),
    path('appointment',user_views.appointment_view,name="appointment"),
    path('get_appointment',user_views.get_appointment,name="get_appointments"),
    path('profile_pic',user_views.profile_pic,name="profile_pic")
]