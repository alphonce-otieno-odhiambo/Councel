from dataclasses import field
from pyexpat import model
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

class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = '__all__'

    def save(self,request):
        details = Details(first_name = self.validated_data['first_name'],last_name = self.validated_data['last_name'],qualities = self.validated_data['qualities'],experiences = self.validated_data['experiences'])
        details.save()
        return details

class GetCounsellorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    details = DetailsSerializer(read_only = True)
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
    
class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['profile_pic']

    def save(self,request):
        profile_pic = Account(profile_pic = self.validated_data['profile_pic'])
        return profile_pic

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
    group = GroupSerializer(read_only=True)
    class Meta:
        model = Client
        fields = '__all__'


class GroupChatSerializer(serializers.ModelSerializer):
    group = GroupSerializer(read_only=True)
    reporter = UserSerializer(read_only=True)
    class Meta:
        model = GroupChat
        fields = '__all__'

    def save(self,request,group):
        groupchat = GroupChat(group = group,reporter = request.user,text = self.validated_data['text'])
        groupchat.save()

class AppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['user']

    def save(self,request):
        appointment = Appointment(user = request.user, date = self.validated_data['date'],topic = self.validated_data['topic'])
        appointment.save()

    
    