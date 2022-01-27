from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .serializers import *
from .forms import *
from django.http.response import HttpResponseRedirect
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
from django.views.generic import ListView
from django.template import Context



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



class CounsellingApi(APIView):
    def get_counselling(self, pk):
        try:
            return Counselling.objects.get(pk=pk)
        except Counselling.DoesNotExist:
            return Http404

    def get(self, request, pk, format = None):
        counselling = self.get_counselling(pk)
        serializers = CounsellingSerializer(counselling)
        return Response(serializers.data)

    def put (self, request, pk, format = None):
        counselling = self.get_counselling(pk)
        serializers = CounsellingSerializer(counselling, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        counselling = self.get_counselling(pk)
        counselling.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)