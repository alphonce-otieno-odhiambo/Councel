from rest_framework import serializers


from .models import Account

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email','password','username']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        account = Account(email=self.validated_data['email'],username = self.validated_data['username'])
        account.set_password(self.validated_data['password'])
        account.save()
        return account

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','email','username','date_joined','last_login','is_counsellor']

        def save():
            counsellor = Account(is_counsellor = False)
            counsellor.save()

class CounsellorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email','password','username','is_counsellor']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        account = Account(email=self.validated_data['email'],username = self.validated_data['username'],is_counsellor = True)
        account.set_password(self.validated_data['password'])
        account.save()
        return account