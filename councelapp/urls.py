from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from rest_framework.authtoken import views
from . import views




urlpatterns=[
    path('clients/', views.ClientsApi.as_view()),
    path('groups/', views.GroupsApi.as_view()),
    path('counsellings/', views.CounsellingsApi.as_view()),
    path('conversations/', views.ConversationsApi.as_view()),
    re_path(r'^client/client-id/(?P<pk>[0-9]+)$', views.ClientApi.as_view()),
    re_path(r'^group/group-id/(?P<pk>[0-9]+)$', views.GroupApi.as_view()),
    re_path(r'^counselling/counselling-id/(?P<pk>[0-9]+)$', views.CounsellingApi.as_view()),
    re_path(r'^conversation/conversation-id/(?P<pk>[0-9]+)$', views.ConversationApi.as_view()),
]