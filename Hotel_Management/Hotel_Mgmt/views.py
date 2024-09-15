from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from .models import Category,FeedBackModel,InventoryItem,Room,StaffProfile,RoomBooking,Suppliers
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer,InventoryItemSerializer,FeedBackSerializer
from rest_framework.exceptions import PermissionDenied



User = get_user_model()

# Create your views here.
#when we use modelviewset it provides all CRUD operations
#but when we use genericvieset with createmodelMixins or other mixins we specifically define the method like whether it is a create or update or delete or get operations

class CategoryViewsets(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]   #here only the admin is able to perform crud operations and user must have login to see the details


class InventoryViewsets(ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class= InventoryItemSerializer
    permission_classes =[IsAuthenticated,IsAdminOrReadOnly]



class FeedBackViewsets(ModelViewSet):
    queryset = FeedBackModel.objects.all()
    serializer_class = FeedBackSerializer
    permission_classes=[IsAuthenticated]   
    
    def get_queryset(self):
        guest= self.request.user
        return self.queryset.filter(guest = guest)


    #only the authorized guest can make changes on the feedback given
    def update(self, request, *args, **kwargs):
        feedback = self.get_object()
        if feedback.guest != self.request.user:
            raise PermissionDenied("you donot have permission to make changes..!!")
        return super().update(request, *args, **kwargs)