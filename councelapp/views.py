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
    
    



