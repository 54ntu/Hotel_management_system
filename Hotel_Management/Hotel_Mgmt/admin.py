from django.contrib import admin
from .models import Category,InventoryItem,RoomBooking,Room

# Register your models here.
@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display =("id","name",)


@admin.register(InventoryItem)
class InventoryItemAdminModel(admin.ModelAdmin):
    list_display=("id","category","name","quantity","description",)


@admin.register(Room)
class RoomsAdminModel(admin.ModelAdmin):
    list_display= ("id","room_no","room_type","availability","price",)


@admin.register(RoomBooking)
class RoomBookingAdminModel(admin.ModelAdmin):
    list_display= ('id','booked_by','check_in_date','check_out_date','room_number','any_request',)