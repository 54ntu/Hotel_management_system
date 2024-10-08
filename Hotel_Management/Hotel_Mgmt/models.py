from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import CustomUserModel


User = get_user_model()

# Create your models here.
class Category(models.Model):
      CATEGORY_CHOICES = (
        ('toiletries', 'Toiletries'),
        ('linens', 'Linens'),
        ('room_supplies', 'Room Supplies'),
    )
      name = models.CharField(choices= CATEGORY_CHOICES  ,max_length=100)

      def __str__(self):
           return self.name



class InventoryItem(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name =models.CharField(max_length=50)
    quantity= models.PositiveIntegerField()
    description = models.CharField(max_length=100)
    reorder_limit= models.PositiveIntegerField(default=5)    # this one is triggered when the quantity becomes equal or less than the reorder limit

    def __str__(self):
         return f"{self.name} {self.category}"
    

    def needs_reorder(self):
         return self.quantity <= self.reorder_limit
    



class Room(models.Model):
     ROOM_CHOICES = [
          ('standard','STANDARD'),
          ('deluxe','DELUXE'),
          ('suite','SUITE'),

     ]

     ROOM_BOOKED ="BOOKED"
     ROOM_AVAILABLE="AVAILABLE"    
     AVAILABILITY_CHOICES =  [
          (ROOM_BOOKED,"BOOKED"),
          (ROOM_AVAILABLE,"AVAILABLE"),
     ]
     room_no = models.PositiveIntegerField(unique=True)
     room_type= models.CharField(choices= ROOM_CHOICES,max_length=50)
     availability = models.CharField(choices=AVAILABILITY_CHOICES,default= ROOM_AVAILABLE,max_length=10)
     price = models.DecimalField(max_digits=6, decimal_places=2)


     def __str__(self):
          return f"{self.room_no}"


class RoomBooking(models.Model):
     BOOKING_SUCCESS ="SUCCESS"
     BOOKING_CANCELLED = "CANCELLED"
     BOOKING_STATUS_CHOICES=[
          (BOOKING_SUCCESS,"SUCCESS"),
          (BOOKING_CANCELLED,"CANCELLED")
     ]
     booked_by = models.ForeignKey(User,on_delete=models.CASCADE)
     check_in_date = models.DateField()
     check_out_date = models.DateField()
     booking_status = models.CharField(choices=BOOKING_STATUS_CHOICES,default=BOOKING_SUCCESS,max_length=15)
     room_number = models.ForeignKey(Room,on_delete= models.CASCADE)
     any_request = models.CharField(max_length=200)

     def __str__(self):
          return f"{self.id} - {self.booked_by}"


class Invoice(models.Model):
     booking  = models.ForeignKey(RoomBooking,on_delete=models.CASCADE)
     amount_due = models.DecimalField(max_digits=10, decimal_places=2)
     total_stay = models.DurationField(default=0)
     issued_date = models.DateTimeField(auto_now_add=True)
     is_paid = models.BooleanField(default= False)


     def __str__(self):
          return f"Invoice {self.id} for booking {self.booking.id}"
     
 

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
     staff_name = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,limit_choices_to={'roles_choices':'staff'},blank=False,null=False)
     staff_role = models.CharField(choices=ROLE_CHOICES,max_length=50)
     assigned_task = models.CharField(max_length=100)
     task_status = models.BooleanField(default=False)
     shift_start= models.TimeField()
     shift_end = models.TimeField()
    


     


class FeedBackModel(models.Model):
     guest =models.ForeignKey(User,on_delete=models.CASCADE)
     experience  = models.TextField(max_length=200)


