from rest_framework.response import Response
from .models import CustomUserModel
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


User = get_user_model()
class GuestRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields =['email','phone_no','password','fullname','city','country',]
        extra_kwargs={
            'password':{'write_only':True},
        }



    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['roles_choices'] = 'guest'
        return User.objects.create(**validated_data)




class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)