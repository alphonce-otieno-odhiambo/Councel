from rest_framework import serializers
from councelapp.models import *

from counsel_users.serializers import UserSerializer

class CounsellorSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Details
        fields = ['first_name','last_name','qualities','work_experience']

    def save(self,request):
        counsellor = Counsellor(user = request.user,first_name=self.validated_data['first_name'],last_name = self.validated_data['last_name'],qualities = self.validated_data['qualities'],work_experience = self.validated_data['work_experience'])
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