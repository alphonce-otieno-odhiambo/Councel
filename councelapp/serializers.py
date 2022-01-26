from rest_framework import serializers
from .models import *
from counsel_users.serializers import UserSerializers

class CounsellorSerializer(serializers.Serializer):
    account = UserSerializers(read_only=True)
    class Meta:
        model = Details
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

class CounselorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model =Counsellor
        fields = ("id", "url", "user","first_name","last_name", "experience","qualities")
class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Appointment
        fields = ("id", "url","first_name", "last_name","email","phone","request","sent_date", "accepted","accepted_date")
class PrescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prescription
        fields = ("id", "url","prid", "clients","counsel","prescription","diagnosis","date")

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "url","counselor", "name")

class ClientProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ("id", "url","first_name", "last_name","age","tel_no","profile_picture")
        
