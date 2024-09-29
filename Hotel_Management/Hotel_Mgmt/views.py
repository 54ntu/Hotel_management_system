from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from .models import Category,FeedBackModel,InventoryItem,Room,StaffProfile,RoomBooking,Suppliers,Invoice
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly,IsStaff
from .serializers import (CategorySerializer,InventoryItemSerializer,FeedBackSerializer,SupplierSerializer,StaffManagementSerializer,RoomAdditionSerializer,RoomAvailabilitySerializer,RoombookingSerailizer,CancelBookingSerializer,BookingUpdateSerializer,InvoiceSerializer,StaffTaskSerializer)
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail
from rest_framework import serializers
from datetime import datetime
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from decimal import Decimal
from roomAvailability import is_room_available



User = get_user_model()

# Create your views here.
#when we use modelviewset it provides all CRUD operations
#but when we use genericvieset with createmodelMixins or other mixins we specifically define the method like whether it is a create or update or delete or get operations


#viewsets for managing the staffProfile and assigning the task to the stafff....
class StaffManagementViewsets(ModelViewSet):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffManagementSerializer
    permission_classes = [IsAuthenticated,IsAdminOrReadOnly]


#viewsets for staff who can see their task assign by the admins and also they can update that task....
class StaffTaskViewsets(ModelViewSet):
    queryset = StaffProfile.objects.all()
    print(f"queryset datas are : {queryset}")
    serializer_class = StaffTaskSerializer
    permission_classes = [IsAuthenticated,IsStaff]

    def get_queryset(self):
        return StaffProfile.objects.filter(staff_name = self.request.user)


    


   
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
        # print(f"queryset datas we are getting : {queryset}")
        serializer_class = RoombookingSerailizer
        permission_classes=[IsAuthenticated]

        def get_queryset(self):
            return RoomBooking.objects.filter(booked_by = self.request.user)

        def create(self, request, *args, **kwargs): 
            serializer = self.get_serializer(data=request.data)
            # print(serializer)
            
            if serializer.is_valid():
                # print(f"serialized datas are : {serializer.validated_data}")
                room = serializer.validated_data['room_number']
                print(f"room data we are gettig is : {room}")
                checked_in_date = serializer.validated_data['check_in_date']
                checked_out_date = serializer.validated_data['check_out_date']
                # print(f"check in date and check out date are : {checked_in_date} {checked_out_date}")


                #convert the both datetime to date
                if isinstance(checked_in_date,datetime):
                        checked_in_date = checked_in_date.date()
                if isinstance(checked_out_date,datetime):
                    checked_out_date = checked_out_date.date()
            
                if is_room_available(room_id=room.id,check_in_date=checked_in_date,check_out_date=checked_out_date):
                    if checked_out_date<checked_in_date:
                        raise serializers.ValidationError("check out date can not be earlier than check in date...!!!")
                    # Use transaction.atomic to ensure all operations are executed as a single transaction
                    with transaction.atomic():
                        self.perform_create(serializer)
                        #update the availability status of the room
                        room.availability= Room.ROOM_BOOKED
                        room.save()

                        # Calculate total price based on the duration of stay
                        duration = (checked_out_date - checked_in_date)
                        total_days = duration.days
                        total_price = Decimal(total_days) * room.price
                        invoice = Invoice.objects.create(booking= serializer.instance, amount_due = total_price,total_stay=duration)

                        subject ='room booking'
                        message="room has been booked successfully..!!"
                        email_from = "hello@gmail.com"
                            
                        recipient_list = [serializer.validated_data['booked_by']]
                        send_mail(subject,message,email_from,recipient_list)
                        return Response({'message':"room booked successfully...!!!",'data':serializer.data,'invoice_id':invoice.id},status= status.HTTP_201_CREATED)
                return Response({"error":"room is not available for the selected date ranges..!!"},status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return super().create(request, *args, **kwargs)
    



        def update(self, request, *args, **kwargs):
            instance = self.get_object()
            print(f"instance value is :  {instance}")
            updated_serializer = BookingUpdateSerializer(data= request.data)
            if updated_serializer.is_valid():

                checked_in_date = updated_serializer.validated_data['check_in_date']
                checked_out_date= updated_serializer.validated_data['check_out_date']
                message_req = updated_serializer.validated_data['any_request']
                email_id = request.data.get('booked_by',instance.booked_by)
            if isinstance(checked_in_date,datetime):
                checked_in_date = checked_in_date.date()
            if isinstance(checked_out_date,datetime):
                checked_out_date = checked_out_date.date()


            if is_room_available(room_id=instance.id, check_in_date=checked_in_date,check_out_date=checked_out_date):
                if checked_out_date<checked_in_date:
                    raise serializers.ValidationError('checkout date cannot be earlier than checkin date...!!')
                
                with transaction.atomic():
                    instance.check_in_date = checked_in_date
                    instance.check_out_date= checked_out_date
                    instance.any_request = message_req
                    instance.save()
                    
                    #calculate the updated stay days and find out the total amount and update the invoice data
                    duration = (checked_out_date - checked_in_date)
                    total_days = duration.days
                    total_amount = Decimal(total_days) * instance.room_number.price
                    #check if invoice is already generated or not if already exist just update that and if not then generate new invoice
                    try:
                        invoice = Invoice.objects.get(booking= instance) #chceck whether invoice is already exists
                        invoice.amount_due = total_amount
                    except Invoice.DoesNotExist:
                        invoice = Invoice(booking=instance,amount_due =total_amount)

                    invoice.save()
                    subject = "room booking updated"
                    message="room booking has been updated...!!"
                    email_from = "hello@gmail.com"
                    # recipient_list = email_id
                    send_mail(subject,message,email_from,[email_id])

                    return Response({
                        'message':'room booking updated successfully...!!',
                        'invoice_id': invoice.id,\
                        "total_due_amount":total_amount,
                        "total_days_of_booking":total_days
                    },status=status.HTTP_200_OK)
            return Response({'message':'room is not available for the selected date ranges...!!'},status=status.HTTP_404_NOT_FOUND)


class CancelBookingViewsets(ModelViewSet):
    queryset = RoomBooking.objects.all()
    serializer_class = CancelBookingSerializer
    permission_classes =[IsAuthenticated]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.booked_by != request.user:
            return Response({
                'message':'you are not valid to perform this action'
            },status=status.HTTP_401_UNAUTHORIZED)
    
        
        # print(f"instance value is : {instance}")
        instance.booking_status = RoomBooking.BOOKING_CANCELLED

        room = instance.room_number
        room.availability = Room.ROOM_AVAILABLE
        instance.delete()
        room.save()

        return Response({
            "message":"booking has been cancelled successfully....!!",
            "booking_id":instance.id
        }, status=status.HTTP_200_OK)
        


class InvoiceViewsets(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

   



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
    