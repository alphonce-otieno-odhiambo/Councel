from django.http import request
from rest_framework import serializers
from councelapp.models import Counsellor


from counsel_users.serializers import UserSerializers

class CounsellorSerializer(serializers.Serializer):
    account = UserSerializers(read_only=True)
    class Meta:
        model = Counsellor
        fields = ['first_name','last_name','qualities','work_experience']

    def save(self,request):
        counsellor = Counsellor(account= request.user,first_name=self.validated_data['first_name'],last_name = self.validated_data['last_name'])
