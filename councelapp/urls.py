from django.urls import path , include
from . import views

from . import views as main_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Councelorprofile', views.CounselorProfileView),
router.register('Councelor', views.CounselorView),


urlpatterns = [
    
    path('counselprofile/', views.counselprofile, name='counselprofile'),
    path('update_profile/<int:id>', views.update_profile, name = 'update_profile'),  
    path('counselor/', views.counselor, name='counselor'),  
    
    path('api/', include(router.urls), name = 'api'),
]