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
    class Meta:
        model = Appointment
        fields = '__all__'

        
class PrescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prescription
        fields = ("id", "url","prid", "clients","counsel","prescription","diagnosis","date")

class GroupSerializer(serializers.Serializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = Group
        fields = '__all__'

    def save(self,request):
        group = Group(name=self.validated_data['name'],admin=request.user,bio=self.validated_data['bio'])
        group.save()

    class GetGroupSerializer(serializers.ModelSerializer):
        """This deals with parsing the neighbourhood model
        Args:
            serializers ([type]): [description]
        """
    admin = UserSerializers()
   
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ['admin']

class ClientProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ("id", "url","first_name", "last_name","age","tel_no","profile_picture")
        
