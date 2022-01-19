from django.shortcuts import render
from .models import Client, Group
from django.http import Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response 
from rest_framework.views import APIView
from .serializers import ClientSerializer, GroupSerializer
from rest_framework import status

# Create your views here.
class ClientsApi(APIView):
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


class ClientApi(APIView):
    def get_client(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
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

    