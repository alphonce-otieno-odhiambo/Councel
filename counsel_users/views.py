from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data['response'] = f"Sign up is successful.Welcome{account.username}"
        return Response(data, status = status.HTTP_201_CREATED)

    else:
        data = serializer.errors
