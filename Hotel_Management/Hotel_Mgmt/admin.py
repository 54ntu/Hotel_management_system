from django.contrib import admin
from .models import Category,InventoryItem,RoomBooking,Room,FeedBackModel,StaffProfile,Suppliers

# Register your models here.
@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display =("id","name",)


@admin.register(InventoryItem)
class InventoryItemAdminModel(admin.ModelAdmin):
    list_display=("id","category","name","quantity","reorder_limit","description",)


@admin.register(Room)
class RoomsAdminModel(admin.ModelAdmin):
    list_display= ("id","room_no","room_type","availability","price",)


@admin.register(RoomBooking)
class RoomBookingAdminModel(admin.ModelAdmin):
    list_display= ('id','booked_by','check_in_date','booking_status','check_out_date','room_number','any_request',)




@admin.register(StaffProfile)
class StaffAdminModel(admin.ModelAdmin):
    list_display= ('id','staff_name','assigned_task','staff_role','shift_start','shift_end',)


@admin.register(Suppliers)
class SuppliersAdminModel(admin.ModelAdmin):
    list_display =('id','name','phone','email','address')



@admin.register(FeedBackModel)
class FeedBackAdminModel(admin.ModelAdmin):
    list_display = ('id','guest','experience',)