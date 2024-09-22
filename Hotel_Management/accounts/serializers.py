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


    def validate_email(self,value):
        if User.objects.filter(email= value).exists():
            raise serializers.ValidationError("This email is already registered.....!!!")
        return value


    def create(self, validated_data):
        
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['roles_choices'] = 'guest'
        return User.objects.create(**validated_data)




class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)



class StaffRegistrationSerializer(serializers.Serializer):
      ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('guest', 'Guest'),
    )
      email =serializers.EmailField(max_length= 50)
      password = serializers.CharField(max_length= 100,write_only = True)
      roles_choices = serializers.ChoiceField(choices=ROLE_CHOICES)




      def validate_email(self,value):
          if User.objects.filter(email= value).exists():
              raise serializers.ValidationError("email already exists....!!!")
          return value
      

      def create(self, validated_data,*args, **kwargs):
          user = User.objects.create_user(
            
              email=validated_data['email'],
              password= validated_data['password'],
              roles_choices= validated_data['roles_choices'],
              is_staff = True

          )
          return user


      