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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage, message
from django.views.generic import ListView
from django.template import Context

from counsel_users.models import Account

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
def counsellor_group_view(request):
    data = {}

    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save(request)
            data['success'] = "The group has been created successfully"
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            serializer.errors
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        groups = Group.objects.filter(group__admin = request.user)
        data = GetGroupSerializer(groups,many=True).data

        return Response(data,status = status.HTTP_200_OK)


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
            serializers.save(self)
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



class CounsellingsApi(APIView):
    def get(self, request, format = None):
        all_counsellings = Counselling.objects.all()
        serializers = CounsellingSerializer(all_counsellings, many=True)
        return Response(serializers.data)

    def post(self, request, format = None):
        serializers = CounsellingSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(self)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



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



class ConversationsApi(APIView):
    def get(self, request, format = None):
        all_conversations = Conversation.objects.all()
        serializers = ConversationSerializer(all_conversations, many=True)
        return Response(serializers.data)

    def post(self, request, format = None):
        serializers = ConversationSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save(self)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



class ConversationApi(APIView):
    def get_conversation(self, pk):
        try:
            return Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Http404

    def get(self, request, pk, format = None):
        conversation = self.get_conversation(pk)
        serializers = ConversationSerializer(conversation)
        return Response(serializers.data)

    def put (self, request, pk, format = None):
        conversation = self.get_conversation(pk)
        serializers = ConversationSerializer(conversation, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        conversation = self.get_conversation(pk)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)