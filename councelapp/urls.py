from django.urls import path
from .views import *
from rest_framework import routers
from . import views
from . import views as client_views

from django.urls import path, include


router = routers.DefaultRouter()
router.register('Appointment', views.AppointmentView),



urlpatterns = [

    # appointment create, update, delete and view details
	path('counsellor/<int:pk>/appointment/', 
		client_views.appointment_create, 
		name = 'counsellee-appointment-create'),
	path('appointment/<int:pk>/', 
		AppointmentDetailView.as_view(),
		name = 'counsellee-appointment-detail'),
	path('appointment/<int:pk>/edit/',
		AppointmentEditView.as_view(success_url="/counsellee/appointments/upcoming/"), 
		name = 'counsellee-appointment-edit'),
	path('appointment/<int:pk>/delete/',
		AppointmentDeleteView.as_view(),
		name = 'counsellee-appointment-delete'),



	# apoointment lists (pending, upcoming, held, archived)
	path('appointments/upcoming/',
		AppointmentsUpcomingView.as_view(),
		name = 'counsellee-appointments-upcoming'),
	path('appointments/requested/',
		AppointmentsRequestedView.as_view(),
		name = 'counsellee-appointments-requested'),
	path('appointments/held/',
		AppointmentsHeldView.as_view(),
		name = 'counsellee-appointments-held'),
	path('appointments/archived/',
		AppointmentsArchivedView.as_view(),
		name = 'counsellee-appointments-archived'),



    
    path('api/', include(router.urls), name = 'api'),

    path('addpres/',views.addpres,name='addpres'),
    path('showpres/',views.showpres,name='showpres'),
    path('showmedhis/',views.showmedhis,name='showmedhis'),

    

]