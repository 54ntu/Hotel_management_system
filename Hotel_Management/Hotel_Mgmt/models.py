from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Category(models.Model):
      CATEGORY_CHOICES = (
        ('toiletries', 'Toiletries'),
        ('linens', 'Linens'),
        ('room_supplies', 'Room Supplies'),
    )
      name = models.CharField(choices= CATEGORY_CHOICES  ,max_length=100)



class InventoryItem(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name =models.CharField(max_length=50)
    quantity= models.PositiveIntegerField()
    description = models.CharField(max_length=100)
    reorder_limit= models.PositiveIntegerField(default=5)    # this one is triggered when the quantity becomes equal or less than the reorder limit




class Room(models.Model):
     ROOM_CHOICES = [
          ('standard','STANDARD'),
          ('deluxe','DELUXE'),
          ('suite','SUITE'),

     ]
     room_no = models.PositiveIntegerField(unique=True)
     room_type= models.CharField(choices= ROOM_CHOICES,max_length=50)
     availability = models.BooleanField(default= True)
     price = models.DecimalField(max_digits=4, decimal_places=2)



class RoomBooking(models.Model):
     booked_by = models.ForeignKey(User,on_delete=models.CASCADE)
     check_in_date = models.DateTimeField()
     check_out_date = models.DateField()
     room_number = models.ForeignKey(Room,on_delete= models.CASCADE)
     any_request = models.CharField(max_length=200)



class Suppliers(models.Model):
     name = models.CharField(max_length=100)
     phone = models.CharField(max_length=15)
     email = models.EmailField(max_length=50,unique=True)
     address = models.CharField(max_length=100)



class StaffProfile(models.Model):
     ROLE_CHOICES =[
          ('frontdesk','FrontDesk'),
          ('housekeeping','HouseKeeping'),
          ('management','Management')
     ]
     staff_name = models.ForeignKey(User,on_delete=models.CASCADE)
     assigned_task = models.CharField(max_length=100)
     staff_role = models.CharField(choices=ROLE_CHOICES,max_length=50)
     shift_start= models.TimeField()
     shift_end = models.TimeField()




class FeedBackModel(models.Model):
     guest =models.ForeignKey(User,on_delete=models.CASCADE)
     experience  = models.TextField(max_length=200)


