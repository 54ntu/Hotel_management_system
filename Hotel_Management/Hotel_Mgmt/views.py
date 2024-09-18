from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from .models import Category,FeedBackModel,InventoryItem,Room,StaffProfile,RoomBooking,Suppliers
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer,InventoryItemSerializer,FeedBackSerializer,SupplierSerializer,StaffManagementSerializer,RoomAdditionSerializer,RoomAvailabilitySerializer,RoombookingSerailizer)
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail



User = get_user_model()

# Create your views here.
#when we use modelviewset it provides all CRUD operations
#but when we use genericvieset with createmodelMixins or other mixins we specifically define the method like whether it is a create or update or delete or get operations



#viewsets for managing the staffProfile and assigning the task to the stafff....
class StaffManagementViewsets(ModelViewSet):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffManagementSerializer

   
    



#this viewset is for managing the category of the inventory item where only the logged in admin can manage this category
class CategoryViewsets(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]   #here only the admin is able to perform crud operations and user must have login to see the details



#this viewset is for managing the inventory of the various category
class InventoryViewsets(ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class= InventoryItemSerializer
    permission_classes =[IsAuthenticated,IsAdminOrReadOnly]


    def update(self, request, *args, **kwargs):
        #call the original update method to perform the actual update operation
        response= super().update(request, *args, **kwargs)

        #get the updated inventory item 
        inventory_item = self.get_object()
        print(f"inventory item which gets updated is : {inventory_item}")

        #now check if the items need reordering
        if inventory_item.needs_reorder():
             self.send_reorder_alert(inventory_item)

        #if reordering is not needed then just return the updated inventory item
        return response
    


    def send_reorder_alert(self,inventory_item):
        subject = 'Reorder Alert : Inventory item is running low..!!!'
        message =(
            f"The inventory item {inventory_item.name} of category {inventory_item.category} is running low. Current quantity :{inventory_item.quantity}"
        )
        email_from  = "xaudharysantey12@gmail.com"
        recipient_list = ['lazypy12@gmail.com']
        send_mail(subject,message,email_from, recipient_list)
    
    
#viewsets for managing room inventory
class RoomViewsets(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomAdditionSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]



class RoomAvailabilityViewsets(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class= RoomAvailabilitySerializer


    def list(self, request, *args, **kwargs):
        available_rooms = self.queryset.filter(availability= Room.ROOM_AVAILABLE)
        serializer = self.get_serializer(available_rooms,many=True)
        return Response({'available_rooms':serializer.data},status=status.HTTP_200_OK)




class RoomBookingViesets(ModelViewSet):
    queryset = RoomBooking.objects.all()
    serializer_class = RoombookingSerailizer
    permission_classes=[IsAuthenticated]


    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            room = serializer.validated_data['room_number']
            print(f"room detail is : {room}")
            if room.availability =="AVAILABLE":
                self.perform_create(serializer)
                #update the availability status of the room
                room.availability= Room.ROOM_BOOKED
                room.save()
                return Response({'message':"room booked successfully...!!!"},status= status.HTTP_201_CREATED)
            return Response({"error":"room is not available..!!"},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        return super().create(request, *args, **kwargs)


class SupplierInfoViewset(ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class  = SupplierSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]


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