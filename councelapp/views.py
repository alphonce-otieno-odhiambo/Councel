from django.shortcuts import render
from .models import Client, Group
from django.http import Http404, JsonResponse

from rest_framework.response import Response 
from rest_framework.views import APIView
from .serializers import ClientSerializer, GroupSerializer
from rest_framework import status

# Create your views here.
class ClientApi(APIView):