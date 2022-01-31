
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
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes



from rest_framework.response import Response
from rest_framework import status


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CounsellorView(request):
    serializer = CounsellorSerializer(data = request.data)
    account = Account.objects.get(user=request.user)
    data = {}
    
    if account.is_counsellor == True:
        if serializer.is_valid():
            serializer.save()
            data['response'] = f'Additional details for {account.username} successfully added'
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    if account.is_counsellor == False:
        data['response'] = 'There is no counsellor registered under those credentials'
        return Response(data,status=status.HTTP_404_NOT_FOUND)
    
    else:
        data['response'] = 'There is no counsellor registered under those credentials'
        return Response(data,status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])   
def counsellor_profile(request):
    data = {}
    profile = Counsellor.objects.get(user = request.user)
    print(profile.user.date_joined)
    data =  CounsellorProfileSerializer(profile).data
    return Response(data,status = status.HTTP_200_OK)

@api_view(['GET'])
def profile(request):
    data = {}
    profile = Counsellor.objects.get(user = request.user)
    print(profile.user.date_joined)
    data =  CounsellorProfileSerializer(profile).data
    return Response(data,status = status.HTTP_200_OK)


@api_view(['POST','GET'])
def group_view(request):
    data = {}

    if request.method == 'GET':
        groups = Group.objects.all()
        data['groups'] = GetGroupSerializer(groups,many=True).data

        return Response(data,status = status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            data['success'] = "The group has been created successfully"
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            serializer.errors
            print(serializer.errors)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_counsellors(request):
    data = {}
    counsellors = Counsellor.objects.filter(user__is_counsellor = True)
    data = CounsellorSerializer(counsellors,many=True).data
    print(counsellors)

    return Response(data,status.HTTP_200_OK)
   
@api_view(['POST'])
def join_counsellor(request,pk):
    data = {}

    client = Client.objects.get(user = request.user)
    new_counsellor = Counsellor.objects.get(pk=pk)
    client.counsellor = new_counsellor
    client.save()
    data['success'] = f"Thank you for joining {new_counsellor.user.username}."
    return Response(data,status = status.HTTP_200_OK)




        

    

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CounsellorView(request):
    serializer = ClientSerializer(data = request.data)
    account = Account.objects.get(user=request.user)
    data = {}
    
    if account.is_client == True:
        if serializer.is_valid():
            serializer.save()
            data['response'] = f'Additional details for {account.username} successfully added'
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    if account.is_client == False:
        data['response'] = 'There is no client registered under those credentials'
        return Response(data,status=status.HTTP_404_NOT_FOUND)
    
    else:
        data['response'] = 'There is no client registered under those credentials'
        return Response(data,status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])   
def counsellor_profile(request):
    data = {}
    profile = ClientProfile.objects.get(user = request.user)
    print(profile.user.date_joined)
    data =  ClientProfileSerializer(profile).data
    return Response(data,status = status.HTTP_200_OK)

@api_view(['GET'])
def profile(request):
    data = {}
    profile = Client.objects.get(user = request.user)
    print(profile.user.date_joined)
    data =  ClientProfileSerializer(profile).data
    return Response(data,status = status.HTTP_200_OK)

@api_view(['GET'])
def counselling(request):
    data = {}
    counselling = Counselling.objects.get(user = request.user)
    print(counselling.user.date_contacted)
    data =  CounsellingSerializer(counselling).data
    return Response(data,status = status.HTTP_200_OK)

@api_view(['GET'])
def conversation(request):
    data = {}
    conversation = Conversation.objects.get(user = request.user)
    print(conversation.user.date_contacted)
    data =  ConversationSerializer(conversation).data
    return Response(data,status = status.HTTP_200_OK)


 # add prescription

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


