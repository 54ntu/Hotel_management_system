from django.shortcuts import render
from rest_framework.response import Response
from .serializers import GuestRegisterationSerializer,UserLoginSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from django.contrib.auth import get_user_model,authenticate
from rest_framework.authtoken.models import Token


User = get_user_model()

# Create your views here.
# class GuestRegistrationView(APIView):
#      def post(self,request):
#           serializer = GuestRegisterationSerializer(data= request.data)
#           if serializer.is_valid():
#                serializer.save()
#                return Response({'message':"guest registered successfully...!!!!"},status=status.HTTP_201_CREATED)
#           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class GuestRegistrationView(GenericViewSet,CreateModelMixin):
      serializer_class = GuestRegisterationSerializer

     
      @action(detail=False,methods=["POST"])
      def login(self, request):
            serializer= UserLoginSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)

            user = authenticate(
                  username = serializer.validated_data['email'],
               password = serializer.validated_data['password']
            )

            if user is not None:
               token, _ = Token.objects.get_or_create(user=user)

               return Response({
                    'token':token.key,
                    'user':serializer.data,
                    'message':'user logged in successfully...!!!!'
               },
               status=status.HTTP_200_OK)
            else:
                 return Response({
                      "errors":"email or password doesnot matched..!!!"
                 },
                 status=status.HTTP_401_UNAUTHORIZED)
