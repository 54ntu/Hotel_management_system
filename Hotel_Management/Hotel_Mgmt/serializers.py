from rest_framework import serializers
from .models import Category,FeedBackModel,InventoryItem,Room,RoomBooking,StaffProfile,Suppliers,Invoice
from accounts.models import CustomUserModel



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
    staff_name = serializers.PrimaryKeyRelatedField(queryset =CustomUserModel.objects.all() )
    class Meta:
        model = StaffProfile
        fields = ['id','staff_name','staff_role','assigned_task','task_status','shift_start','shift_end']


    def validate_staff_name(self,value):
        if value.roles_choices != 'staff':
            raise serializers.ValidationError("the selected user is not a staff..!!")
        

         #check if the staff has any uncompleted task or not (task_status=false)
        if StaffProfile.objects.filter(staff_name= value, task_status=False).exists():
            raise serializers.ValidationError(f"{value} already has uncompleted task. Assign task only after completing the task.")
        
        return value

       
        
class StaffTaskSerializer(serializers.ModelSerializer):
    staff_name = serializers.StringRelatedField()
    class Meta:
        model = StaffProfile
        fields = ['id','staff_name','staff_role','assigned_task','task_status','shift_start','shift_end']






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
   
    class Meta:
        model = RoomBooking
        fields = ['id','booked_by','check_in_date','check_out_date','room_number','any_request','booking_status']
        # here in room_number we are actually getting the foreignkey id 


class BookingUpdateSerializer(serializers.Serializer):
    check_in_date = serializers.DateField()
    check_out_date = serializers.DateField()
    any_request = serializers.CharField()


class CancelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields =[]


class InvoiceSerializer(serializers.ModelSerializer):
    booking = RoombookingSerailizer()
    class Meta:
        model = Invoice
        fields =['id','booking','amount_due','issued_date','is_paid',]
 