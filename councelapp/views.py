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
   
@api_view(['GET'])
def get_single_counsellor(request,pk):

    counsellor = Counsellor.objects.get(pk=pk) 
    data = CounsellorSerializer(counsellor,many=False).data
    print(data)

    return Response(data,status= status.HTTP_200_OK)

@api_view(['POST'])
def join_counsellor(request,pk):
    data = {}

    client = Client.objects.get(user = request.user)
    new_counsellor = Counsellor.objects.get(pk=pk)
    client.counsellor = new_counsellor
    client.save()
    data['success'] = f"Thank you for joining {new_counsellor.user.username}."
    return Response(data,status = status.HTTP_200_OK)