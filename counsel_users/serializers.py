from rest_framework import serializers


from .models import Account,MyAccountManager

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email','password','username']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        account = Account(email=self.validated_data['email'],username = self.validated_data['username'],is_counsellor = False)
        account.set_password(self.validated_data['password'])
        print(account.is_counsellor)
        account.save()
        return account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['profile_pic','id','email','username','date_joined','last_login','is_counsellor']

class PicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['profile_pic']

    def save(self):
        pic = Account(profile_pic = self.validated_data['profile_pic'])
        pic.save()
           

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
        print(account.is_counsellor)
        return account
       