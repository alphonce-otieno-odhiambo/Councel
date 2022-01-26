from rest_framework import serializers
from .models import ClientProfile, Group
from .models import *
from counsel_users.serializers import UserSerializers

class ClientSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    class Meta:
        model = ClientProfile
        fields = ('id', 'first_name', 'last_name', 'age', 'tel_no', 'groups', 'profile_picture')


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


class GetGroupSerializer(serializers.ModelSerializer):
    admin = UserSerializers()
   
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['admin']


class CounselorProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CounselorProfile
        fields = ("id", "url","counselor", "bio","profile_pic")

class CounselorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model =Counsellor
        fields = ("id", "url", "user","first_name","last_name", "experience","qualities")
        
