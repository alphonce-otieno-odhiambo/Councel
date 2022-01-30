from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
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
def group_view(request):
    data = {}

    if request.method == 'GET':
        groups = Group.objects.filter(group__admin = request.user)
        data = GetGroupSerializer(groups,many=True).data

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
    counsellor = Account.objects.filter(is_counsellor=True)