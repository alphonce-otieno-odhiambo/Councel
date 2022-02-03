from rest_framework import serializers
from .models import ClientProfile, Group
from .models import *
from counsel_users.serializers import UserSerializers

from counsel_users.serializers import UserSerializers

class CounsellorSerializer(serializers.Serializer):
    account = UserSerializers(read_only=True)
    class Meta:
        model = Counsellor
        fields = ['first_name','last_name','qualities','work_experience']

    def save(self,request):
        counsellor = Counsellor(account= request.user,first_name=self.validated_data['first_name'],last_name = self.validated_data['last_name'],qualities = self.validated_data['qualities'],work_experience = self.validated_data['work_experience'])
        counsellor.save()
        return counsellor 

class CounsellorProfileSerializer(serializers.ModelSerializer):
    details = CounsellorSerializer(read_only=True)
    user = UserSerializers(read_only=True)
    class Meta:
        model = Counsellor
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = Group
        fields = '__all__'

    def save(self,request):
        group = Group(name=self.validated_data['name'],admin=request.user,bio=self.validated_data['bio'])
        group.save()


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class CounsellingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counselling
        fields = '__all__'


class GetGroupSerializer(serializers.ModelSerializer):
    admin = UserSerializers()
   
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['admin']


class CounsellorSerializer(serializers.Serializer):
    account = UserSerializers(read_only=True)
    class Meta:
        model = Counsellor
        fields = '__all__'

    def save(self,request):
        counsellor = Counsellor(account= request.user,first_name=self.validated_data['first_name'],last_name = self.validated_data['last_name'],qualities = self.validated_data['qualities'],work_experience = self.validated_data['experience'])
        counsellor.save()
        return counsellor 

class CounsellorProfileSerializer(serializers.ModelSerializer):
    details = CounsellorSerializer(read_only=True)
    user = UserSerializers(read_only=True)
    class Meta:
        model =Counsellor
        fields = ("id", "url", "user","first_name","last_name", "experience","qualities")
        
