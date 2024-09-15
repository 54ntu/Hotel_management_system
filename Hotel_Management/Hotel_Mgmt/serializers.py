from rest_framework import serializers
from .models import Category,FeedBackModel,InventoryItem,Room,RoomBooking,StaffProfile,Suppliers



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields  = ['name',]


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['category','name','quantity','description']


class FeedBackSerializer(serializers.ModelSerializer):
    guest = serializers.HiddenField(default= serializers.CurrentUserDefault)  
    class Meta:
        model = FeedBackModel
        fields  = ['guest','experience']