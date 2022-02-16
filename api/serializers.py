from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from .models import User

class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ['username', 'email', 'password', 'password2', 'address']
        model = User

        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    
    def validate(self, data):
        # print(data.get("email"))
        # print("---------------------------")
        # print(data)
        if data.get('email') == None or data.get("email") == '' or User.objects.filter(email=data.get('email').lower()).exists():
            raise serializers.ValidationError("Enter a valid email")

        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Both password must be same.")

        return data

    def save(self):
        user = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            address = self.validated_data['address']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()

        return user

class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attr):
        username = attr.get('username')
        password = attr.get("password")
        self.user = None

        user_count = User.objects.filter(username=username).count()

        if user_count != 0:
            self.user = User.objects.get(username=username).username
        else:
            user_count = User.objects.filter(email=username).count()
            if user_count==0:
                raise serializers.ValidationError("Invalid Credentials!")
            else:
                self.user = User.objects.get(email=username).username
        username = self.user

        if username and password:
            self.user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not self.user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')
        
        data = {}
        refresh = self.get_token(self.user)
        # print("---------------------------")
        # print(refresh, refresh.access_token)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['pk', 'username', 'email', 'address']
        model = User