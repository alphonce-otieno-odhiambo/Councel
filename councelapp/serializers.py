from rest_framework import serializers
from .models import *
from counsel_users.serializers import UserSerializers

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
        model = Counsellor
        fields = '__all__'


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = Appointment
        fields = '__all__'



class GroupSerializer(serializers.Serializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = Group
        fields = '__all__'

    def save(self,request):
        group = Group(name=self.validated_data['name'],admin=request.user,bio=self.validated_data['bio'])
        group.save()

    class GetGroupSerializer(serializers.ModelSerializer):
        """This deals with parsing the clients model
        Args:
            serializers ([type]): [description]
        """
    admin = UserSerializers()
   
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['admin']

class ClientSerializer(serializers.Serializer):
    account = UserSerializers(read_only=True)
    class Meta:
        model = Client
        fields = '__all__'

    def save(self,request):
        client = Client(user= request.user,counsellor=self.validated_data['counsellor'])
        client.save()
        return client 

class ClientProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = ClientProfile
        fields = '__all__'

class CounsellingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Counselling
        fields = ["id","url","counsellor","client","date_contacted"]

class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conversation
        fields = ["id","url","counsellor","client"]


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conversation
        fields = ["id","url","conversation","text","time"]