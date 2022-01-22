from django.urls import path
from counsel_users import views as user_views
from rest_framework.authtoken import views
from rest_framework.authtoken import views as special_views

from .views import *

urlpatterns = [
    path('counsellor_details',user_views.counsellor_view,name='counsellor')
]