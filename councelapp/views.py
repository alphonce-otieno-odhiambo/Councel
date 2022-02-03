from datetime import datetime
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime

from .serializers import *
from .pusher import pusher_client
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
def current_date(request):
    current_date = datetime.datetime.now()
    print(current_date)
    return Response(current_date,status = status.HTTP_200_OK)

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
    profile = Client.objects.get(user = request.user)
    print(profile.user.date_joined)
    data =  ClientProfileSerializer(profile).data
    return Response(data,status = status.HTTP_200_OK)


@api_view(['POST','GET'])
def group_view(request):
    data = {}

    if request.method == 'GET':
        groups = Group.objects.all()
        data['groups'] = GetGroupSerializer(groups,many=True).data

        return Response(data,status = status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            data['success'] = "The group has been created successfully"
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            serializer.errors
            print(serializer.errors)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_counsellors(request):
    data = {}
    counsellors = Counsellor.objects.filter(user__is_counsellor = True)
    data = GetCounsellorSerializer(counsellors,many=True).data

    return Response(data,status.HTTP_200_OK)

@api_view(["GET"])
def clients_counsellor(request):
    data = {}
    client = Client.objects.get(user=request.user)
    print(client.counsellor)
    data = ClientProfileSerializer(client).data
    return Response(data,status = status.HTTP_200_OK)

@api_view(['GET'])

def get_clients(request,pk):
    """
    This parses the request to get the users in a certain neighbourhood
    Args:
        request ([type]): [description]
        pk ([type]): [description]
    """
    data = {}
    clients = Client.get_clients(pk)
    data['clients'] = ClientProfileSerializer(clients,many=True).data
    return Response(data,status = status.HTTP_200_OK)


@api_view(['POST'])
def join_counsellor(request,pk):
    data = {}

    client = Client.objects.get(user = request.user)
    new_counsellor = Counsellor.objects.get(pk=pk)
    client.counsellor = new_counsellor
    client.save()
    data['success'] = f"Congratulations.{new_counsellor.username} is now your counsellor."
    return Response(data,status = status.HTTP_200_OK)

@api_view(['POST'])
def join_counsellor(request,pk):
    data = {}

    client = Client.objects.get(user = request.user)
    new_counsellor = Counsellor.objects.get(pk=pk)
    client.counsellor = new_counsellor
    client.save()
    data['success'] = f"Thank you for joining {new_counsellor.user.username}."
    return Response(data,status = status.HTTP_200_OK)

@api_view(['GET'])
def get_group(request):
    client = Client.objects.get(user=request.user)
    print(client.group)
    data = ClientProfileSerializer(client).data
    return Response(data,status = status.HTTP_200_OK) 

@api_view(['POST'])
def join_group(request,pk):
    data = {}

    client = Client.objects.get(user = request.user)
    new_group = Group.objects.get(pk=pk)
    client.group = new_group
    client.save()
    data['success'] = f"Welcome to {new_group.name}" 
    return Response(data,status = status.HTTP_200_OK)

@api_view(['GET','POST'])
def group_chat(request,pk):
    data = {}

    try:
        group = Group.objects.get(pk=pk)
    except :

        data['not found'] = "The group was not found"
        return Response(data,status = status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = GroupChatSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save(request,group)
            data['success'] = "The message was successfully sent"
            return Response(data,status = status.HTTP_200_OK)

        else:
            data = serializer.errors
            print(data)
            return Response(data,status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        messages = GroupChat.get_messages(pk)
        data = GroupChatSerializer(messages,many=True).data

        return Response(data,status= status.HTTP_200_OK)


class MessageAPIView(APIView):

    def post(self, request):
        pusher_client.trigger('chat', 'message', {
            'message':request.data['message']
        })

        return Response([])

@api_view(['POST','GET'])
def appointment_view(request):
    data = {}

    if request.method == 'GET':
        appointments = Appointment.objects.all()
        data['appointments'] = AppointmentSerializer(appointments,many=True).data

        return Response(data,status = status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            data['success'] = "The appointment has been created successfully"
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            serializer.errors
            print(serializer.errors)
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_appointment(request):
    data = {}
   
    appointments = Appointment.objects.all()
    data['appointments'] = AppointmentSerializer(appointments,many=True).data
    return Response(data,status = status.HTTP_200_OK)

@api_view(['POST'])
def profile_pic(request):
    data = {}

    serializer = ProfilePicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(request)
        data['success'] = "The pic has been posted successfully"
        return Response(data,status = status.HTTP_201_CREATED)