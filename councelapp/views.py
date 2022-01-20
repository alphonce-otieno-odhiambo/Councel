
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .serializers import *
from .forms import *
from . models import *
from rest_framework.response import Response
from rest_framework import status


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
        
class CounselorProfileView(viewsets.ModelViewSet):
    queryset = CounselorProfile.objects.all()
    serializer_class = CounselorProfileSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)