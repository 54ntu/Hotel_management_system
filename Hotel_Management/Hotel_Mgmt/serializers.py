from rest_framework import serializers
from .models import Category,FeedBackModel,InventoryItem,Room,RoomBooking,StaffProfile,Suppliers



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields  = ['id','name',]


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id','category','name','quantity','description']


class FeedBackSerializer(serializers.ModelSerializer):
    guest = serializers.HiddenField(default= serializers.CurrentUserDefault)  
    class Meta:
        model = FeedBackModel
        fields  = ['id','guest','experience']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields =['id','name','phone','email','address']



class StaffManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = ['id','staff_name','staff_role','assigned_task','task_status','shift_start','shift_end']