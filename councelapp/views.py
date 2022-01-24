
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.test import Client
from rest_framework import viewsets, permissions
from .serializers import *
from .forms import *
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.contrib import messages
from .models import Appointment
from django.views.generic import ListView
import datetime
from django.template import Context
from django.template.loader import render_to_string, get_template
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required



from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@api_view(['GET'])
def counselprofile(request):

    current_user = request.user
    data = {}
    profile = CounselorProfile.objects.filter(user_id=current_user.id).first()           
    return Response(data,status = status.HTTP_200_OK)
@api_view(['POST'])
def update_profile(request,id):
    user = User.objects.get(id=id)
    profile = CounselorProfile.objects.get(user_id = user)
    form = CounselorProfile(instance=profile)
    if request.method == "POST":
            form = CounselorProfile(request.POST,request.FILES,instance=profile)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.save()
                data = {}
                return Response(data,status = status.HTTP_200_OK)
    else:
        form = CounselorProfile()
        data = {}
        return Response(data,status = status.HTTP_200_OK)
@api_view(['GET'])
def counselor(request):
    current_user = request.user
    data = {}
    counselordetails = Counselor.objects.filter(user_id=current_user.id).first()           
    return Response(data,status = status.HTTP_200_OK)

        
class CounselorProfileView(viewsets.ModelViewSet):
    queryset = CounselorProfile.objects.all()
    serializer_class = CounselorProfileSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)

class CounselorView(viewsets.ModelViewSet):
    queryset = Counselor.objects.all()
    serializer_class = CounselorSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)
@api_view(['POST'])
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
@api_view(['POST'])
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
@api_view(['POST'])
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

    @api_view(['GET'])
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({   
            "title":"Manage Appointments"
        })
        return context


 # add prescription
@api_view(['POST'])
@login_required(login_url="/accounts/login/")
def addpres(request):
    cons=Counselor.objects.filter(user=request.user).first()
    clnt=Client.objects.all()
    if request.method=='POST':
        patname=request.POST['pat']
        pres=request.POST['pres']
        us=User.objects.filter(first_name=patname).first()
        clnt=Client.objects.filter(user=us).first()
        diag=request.POST['diag']
        prescript=Prescription(prescription=pres,client=clnt,counselor=cons,diagnosis=diag)
        prescript.save()
        return redirect("showpres")
    return render(request,'prescriptions/addpres.html',{'clnt':clnt})
    # show prescription
@api_view(['GET'])
def showpres(request):
    pre=Prescription.objects.all()
    return render(request,'prescriptions/showpres.html',{'pre':pre})
    # show medical history
@api_view(['GET'])
def showmedhis(request):
    cons=Client.objects.filter(user=request.user).first()
    pre=Prescription.objects.filter(client=cons).all()

# 
class AppointmentView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)
class PrescriptView(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)


