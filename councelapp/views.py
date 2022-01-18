from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import *
from django.http.response import JsonResponse
from .forms import *
from . models import *

# Create your views here.
class PofileView(viewsets.ModelViewSet):
    queryset = CounselorProfile.objects.all()
    serializer_class = CounselorProfileSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)