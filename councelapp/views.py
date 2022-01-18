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
def counselprofile(request):
    current_user = request.user
    profile = CounselorProfile.objects.filter(user_id=current_user.id).first()           
    return render(request, "profile/profile.html", {"profile": profile, })

def update_profile(request,id):
    user = User.objects.get(id=id)
    profile = CounselorProfile.objects.get(user_id = user)
    form = CounselorProfile(instance=profile)
    if request.method == "POST":
            form = CounselorProfile(request.POST,request.FILES,instance=profile)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.save()
                return redirect('profile')
    else:
        form = CounselorProfile()
    return render(request, 'profile/profile_form.html', {"form":form})
class CounselorProfileView(viewsets.ModelViewSet):
    queryset = CounselorProfile.objects.all()
    serializer_class = CounselorProfileSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly)