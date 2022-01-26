from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.contrib import messages
from .models import Appointment
from django.views.generic import ListView
import datetime
from django.template import Context
from django.template.loader import render_to_string, get_template

from rest_framework import viewsets, permissions
from .serializers import *
from . models import *
from rest_framework.response import Response
from rest_framework import status


from django.views.generic import UpdateView
from django.views.generic import DeleteView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.

# Appointment Lists (upcoming, requested, held, archived)
class AppointmentsUpcomingView(ListView):
	model = Appointment
	template_name = 'client/appointments_upcoming.html'
	context_object_name = 'appointments'
	paginate_by = 5 

	def get_queryset(self):
		client = self.request.user.client
		return Appointment.objects.filter(
			counsellee=client).filter(
			requested=True).filter(
			fixed=True).filter(
			held=False).filter(
			counsellee_archived=False)


class AppointmentsRequestedView(ListView):
	model = Appointment
	template_name = 'client/appointments_requested.html'
	context_object_name = 'appointments'
	paginate_by = 5 

	def get_queryset(self):
		client = self.request.user.counsellee
		return Appointment.objects.filter(
			client=client).filter(
			requested=True).filter(
			fixed=False).filter(
			held=False).filter(
			client_archived=False)

class AppointmentsArchivedView(ListView):
	model = Appointment
	template_name = 'counsellees/appointments_archived.html'
	context_object_name = 'appointments'
	paginate_by = 5 

	def get_queryset(self):
		counsellee = self.request.user.counsellee
		return Appointment.objects.filter(
			counsellee=counsellee).filter(
			counsellee_archived=True)


# General Appointment Views (create, detail, edit, delete)
def appointment_create(request, pk):
	counsellee = request.user.counsellee
	counsellor = Counsellor.objects.get(pk=pk)
	if request.method == 'POST':
		form = AppointmentCreateForm(request.POST)
		if form.is_valid():			
			appointment = form.save(commit=False)
			appointment.counsellee = counsellee
			appointment.counsellor = counsellor
			appointment.save()
			# record contacted status
			if not Counselling.objects.filter(counsellor=counsellor, counsellee=counsellee).exists():
				new_record = Counselling(counsellor = counsellor, counsellee = counsellee) 
				new_record.save()
			
			messages.success(request, f'Appointment requested successfully!')
			return redirect('counsellee-appointments-requested')
	else:
		form = AppointmentCreateForm()
	context = {'form': form}
	return render(request, 'counsellees/appointment_create.html', context)




# Prescription

    # add prescription
# @login_required(login_url="/accounts/login/")
# def addpres(request):
#     con=Counsellor.objects.filter(user=request.user).first()
#     c=Client.objects.all()
#     if request.method=='POST':
#         clntname=request.POST['pat']
#         pres=request.POST['pres']
#         us=User.objects.filter(first_name=clntname).first()
#         clnt=Client.objects.filter(user=us).first()
#         dia=request.POST['dia']
#         prescript=Prescription(prescription=pres,client=clnt,counsellor=con,diagnosis=dia)
#         prescript.save()
#         return redirect("showpres")
#     return render(request,'prescriptions/addpres.html',{'c':c})

    # show prescription
# @login_required(login_url="/accounts/login/")
# def showpres(request):
#     pre=Prescription.objects.all()
#     return render(request,'prescriptions/showpres.html',{'pre':pre})

    # show medical history
# @login_required(login_url="/accounts/login/")
# def showmedhis(request):
#     con=Client.objects.filter(user=request.user).first()
#     pre=Prescription.objects.filter(client=con).all()
#     return render(request,'prescriptions/showmedhis.html',{'pre':pre})



