
from django.contrib import messages
from django.contrib.auth.models import User
# from django.test import Client
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
from rest_framework.views import APIView
from django.http import Http404, HttpResponse



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
    counselordetails = Counsellor.objects.filter(user_id=current_user.id).first()           
    return Response(data,status = status.HTTP_200_OK)

        

    
@api_view(['POST'])
class HomeTemplateView(TemplateView):
    
    
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
class AppointmentsAPI(APIView):
    def get (self, request, format=None):
        all_appointments = Appointment.objects.all()
        serializers = AppointmentSerializer(all_appointments, many=True)
        return Response(serializers.data)

# POST
    def post (self, request, format=None):
        serializers = AppointmentSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# manageappointment
@api_view(['POST'])
class ManageAppointmentTemplateView(ListView):
    
    model = Appointment
    context_object_name = "appointments"
    login_required = True
   


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
class AppointmentAPI(APIView):
    def get_appointment(self,pk):
        try : 
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Http404


    def get(self,request,pk,format=None):
        appointment = self.get_appointment(pk)
        serializers= AppointmentSerializer(appointment)
        return Response(serializers.data)

        # update
    def put(self,request,pk,format=None):
        appointment = self.get_appointment(pk)
        serializers = AppointmentSerializer(appointment, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response (serializers.data)
        else : 
            return  Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


            # delete
    def delete (self,request,pk,format=None):
        appointment = self.get_appointment(pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



 # add prescription
@api_view(['POST'])
@login_required(login_url="/accounts/login/")
def addpres(request):
    cons=Counsellor.objects.filter(user=request.user).first()
    clnt=ClientProfile.objects.all()
    if request.method=='POST':
        patname=request.POST['pat']
        pres=request.POST['pres']
        us=User.objects.filter(first_name=patname).first()
        clnt=ClientProfile.objects.filter(user=us).first()
        diag=request.POST['diag']
        
        data = {}
        return Response(data,status = status.HTTP_200_OK)
    # show prescription
# @api_view(['GET'])
# def showpres(request):
#     pre=Prescription.objects.all()
#     data = {}
#     return Response(data,status = status.HTTP_200_OK)
#     # show medical history
# @api_view(['GET'])
# def showmedhis(request):
#     cons=ClientProfile.objects.filter(user=request.user).first()
#     pre=Prescription.objects.filter(client=cons).all()


class AppointmentView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)
# class PrescriptView(viewsets.ModelViewSet):
#     queryset = Prescription.objects.all()
#     serializer_class = PrescriptionSerializer
#     permission_class = (permissions.IsAuthenticatedOrReadOnly)

class CounselorProfView(viewsets.ModelViewSet):
    queryset = CounselorProfile.objects.all()
    serializer_class = CounsellorProfileSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)

class CounselorView(viewsets.ModelViewSet):
    queryset = Counsellor.objects.all()
    serializer_class = CounsellorSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)

class  GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)

class  ClientProfileView(viewsets.ModelViewSet):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)


