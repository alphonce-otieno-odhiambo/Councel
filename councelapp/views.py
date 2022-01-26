
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .serializers import *
from .forms import *
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.http import Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.views.generic import ListView
import datetime
from django.template import Context
from django.template.loader import render_to_string, get_template



# Create your views here.
class ClientsApi(APIView):
    def get(self, request, format = None):
        all_clients = ClientProfile.objects.all()
        serializers = ClientSerializer(all_clients, many=True)
        return Response(serializers.data)

    def post(self, request, format = None):
        serializers = ClientSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientApi(APIView):
    def get_client(self, pk):
        try:
            return ClientProfile.objects.get(pk=pk)
        except ClientProfile.DoesNotExist:
            return Http404

    def get(self, request, pk, format = None):
        client = self.get_client(pk)
        serializers = ClientSerializer(client)
        return Response(serializers.data)

    def put (self, request, pk, format = None):
        client = self.get_client(pk)
        serializers = ClientSerializer(client, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        client = self.get_client(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class GroupsApi(APIView):
    def get(self, request, format = None):
        all_groups = Group.objects.all()
        serializers = GroupSerializer(all_groups, many=True)
        return Response(serializers.data)

    def post(self, request, format = None):
        serializers = GroupSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupApi(APIView):
    def get_group(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Http404

    def get(self, request, pk, format = None):
        group = self.get_group(pk)
        serializers = GroupSerializer(group)
        return Response(serializers.data)

    def put (self, request, pk, format = None):
        group = self.get_group(pk)
        serializers = GroupSerializer(group, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        group = self.get_group(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# Create your views here.
def counselprofile(request):
    current_user = request.user
    data = {}
    profile = CounselorProfile.objects.filter(user_id=current_user.id).first()           
    return Response(data,status = status.HTTP_200_OK)

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
