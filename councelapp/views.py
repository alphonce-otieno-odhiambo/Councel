from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
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

class HomeTemplateView(TemplateView):
    template_name = "index.html"
    
    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email = EmailMessage(
            subject= f"{name} from counsellor.",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )
        email.send()
        return HttpResponse("Email sent successfully!")

# appointment
class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("fname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)



# manageappointment

class ManageAppointmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3


    def post(self, request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        appointment.save()

        data = {
            "fname":appointment.first_name,
            "date":date,
        }

        message = get_template('email.html').render(data)
        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype = "html"
        email.send()

        messages.add_message(request, messages.SUCCESS, f"You accepted the appointment of {appointment.first_name}")
        return HttpResponseRedirect(request.path)


    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({   
            "title":"Manage Appointments"
        })
        return context



# 
class AppointmentView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)




# 
class AppointmentEdit(UpdateView):
	model = Appointment
	template_name = "appointment_form.html"
	success_url = reverse_lazy('appointment_list')
	fields = '__all__'
	def get_object(self, queryset=None):
		obj = super(AppointmentEdit, self).get_object()
		return obj

appointment_edit = AppointmentEdit.as_view()

class AppointmentDelete(DeleteView):
	model = Appointment
	template_name = "appointment_delete.html"
	success_url = reverse_lazy('appointment_list')
	def get_object(self, queryset=None):
		obj = super(AppointmentDelete, self).get_object()
		return obj

appointment_delete = AppointmentDelete.as_view()


# Prescription

    # add prescription
@login_required(login_url="/accounts/login/")
def addpres(request):
    doc=Doctor.objects.filter(user=request.user).first()
    p=Patient.objects.all()
    if request.method=='POST':
        patname=request.POST['pat']
        pres=request.POST['pres']
        us=User.objects.filter(first_name=patname).first()
        pat=Patient.objects.filter(user=us).first()
        dis=request.POST['dis']
        prescript=Prescription(prescription=pres,patient=pat,doctor=doc,disease=dis)
        prescript.save()
        return redirect("showpres")
    return render(request,'prescriptions/addpres.html',{'p':p})

    # show prescription
@login_required(login_url="/accounts/login/")
def showpres(request):
    pre=Prescription.objects.all()
    return render(request,'prescriptions/showpres.html',{'pre':pre})

    # show medical history
@login_required(login_url="/accounts/login/")
def showmedhis(request):
    doc=Patient.objects.filter(user=request.user).first()
    pre=Prescription.objects.filter(patient=doc).all()
    return render(request,'prescriptions/showmedhis.html',{'pre':pre})



