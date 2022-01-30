from unicodedata import name
from django.urls import path
from councelapp import views as user_views
from rest_framework.authtoken import views
from rest_framework.authtoken import views as special_views

from .views import *

urlpatterns = [
    path('counsellor_details',user_views.CounsellorView,name='counsellor'),
    path('counsellors',user_views.get_counsellors,name="counsellors"),
    path('counsellor_profile',user_views.counsellor_profile,name='profile'),
    path('client_profile',user_views.profile,name="client_profile"),
    path('group_view',user_views.group_view,name='counsellor_groups')
]