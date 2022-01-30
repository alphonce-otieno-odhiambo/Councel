from rest_framework import serializers
from councelapp.models import *

from counsel_users.serializers import UserSerializer

class CounsellorSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Counsellor
        fields = ['profile_pic']

    def save(self,request):
        counsellor = Counsellor(user = request.user,profile_pic=self.validated_data['profile_pic'])
        counsellor.save()
        return counsellor 

class GetCounsellorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Counsellor
        fields = '__all__'
        

class CounsellorProfileSerializer(serializers.ModelSerializer):
    details = CounsellorSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Counsellor
        fields = '__all__'
    
    def save(self,request):
        pic = Counsellor
    
        

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
            model = Group
            fields = '__all__'
            read_only_fields = ['admin']

    def save(self,request):
        print(request.user)
        group = Group(name = self.validated_data['name'],admin = request.user,bio = self.validated_data['bio'])
        group.save()

class GetGroupSerializer(serializers.ModelSerializer):
    """This deals with parsing the neighbourhood model
    Args:
        serializers ([type]): [description]
    """
    admin = UserSerializer()
   
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['admin']

class ClientProfileSerializer(serializers.ModelSerializer):
    counsellor = CounsellorProfileSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Counsellor
        fields = '__all__'