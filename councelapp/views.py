from django.shortcuts import render
from .models import Client, Group
from django.http import Http404, JsonResponse

from rest_framework.response import Response 
from rest_framework.views import APIView
from .serializers import ClientSerializer, GroupSerializer
from rest_framework import status

# Create your views here.
class ClientApi(APIView):
    def get(self, request, format = None):
        all_clients = Client.objects.all()
        serializers = ClientSerializer(all_clients, many=True)
        return Response(serializers.data)

    def post(self, request, format = None):
        serializers = ClientSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)