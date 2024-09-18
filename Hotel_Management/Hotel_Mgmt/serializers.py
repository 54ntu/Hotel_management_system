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


    def validate_staff_name(self,value):
        if value.roles_choices != 'staff':
            raise serializers.ValidationError("the selected user is not valid staff..!!")
        return value
    


class RoomAdditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','room_no','room_type','availability','price']

class RoomAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields =['id','availability','room_no','room_type','price']


class RoombookingSerailizer(serializers.ModelSerializer):
    booked_by = serializers.CharField(default = serializers.CurrentUserDefault())
    # room_number = serializers.SerializerMethodField()
    class Meta:
        model = RoomBooking
        fields = ['booked_by','check_in_date','check_out_date','room_number','any_request']