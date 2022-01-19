from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from . import views

urlpatterns=[
    path('api/clients/', views.ClientsApi.as_view()),
    re_path(r'^api/client/client-id/(?P<pk>[0-9]+)$', views.ClientApi.as_view()),
]