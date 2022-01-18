from django.urls import path , include
from . import views

from . import views as main_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('department', views.CounselorProfileView),


urlpatterns = [
    path('', views.home , name = 'home'),
    path('counselprofile/', views.counselprofile, name='counselprofile'),
    path('update_profile/<int:id>', views.update_profile, name = 'update_profile'),    
    
    path('apis/', include(router.urls), name = 'apis'),
]