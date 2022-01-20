from unicodedata import name
from django.urls import path
from counsel_users import views as user_views
from rest_framework.authtoken import views
from rest_framework.authtoken import views as special_views

from .views import *


urlpatterns = [
    path('register',user_views.registration_view,name="register"),
    path('login', special_views.obtain_auth_token),
    path('counsellor_registration',user_views.counsellor_view,name="counsellor"),
    path('counsellor_login',special_views.obtain_auth_token),
    path('delete/<int:pk>',user_views.delete_user,name="delete"),
]
