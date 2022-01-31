from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
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

from rest_framework.views import APIView


# Create your views here.
# GET
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

# single appointment
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



# Prescription

    # add prescription
@login_required(login_url="/accounts/login/")
def addpres(request):
    con=Counsellor.objects.filter(user=request.user).first()
    c=Client.objects.all()
    if request.method=='POST':
        clntname=request.POST['pat']
        pres=request.POST['pres']
        us=User.objects.filter(first_name=clntname).first()
        clnt=Client.objects.filter(user=us).first()
        dia=request.POST['dia']
        prescript=Prescription(prescription=pres,client=clnt,counsellor=con,diagnosis=dia)
        prescript.save()
        return redirect("showpres")
    return render(request,'prescriptions/addpres.html',{'c':c})

    # show prescription
@login_required(login_url="/accounts/login/")
def showpres(request):
    pre=Prescription.objects.all()
    return render(request,'prescriptions/showpres.html',{'pre':pre})

    # show medical history
@login_required(login_url="/accounts/login/")
def showmedhis(request):
    con=Client.objects.filter(user=request.user).first()
    pre=Prescription.objects.filter(client=con).all()
    return render(request,'prescriptions/showmedhis.html',{'pre':pre})







