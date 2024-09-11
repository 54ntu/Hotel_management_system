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



class Rooms(models.Model):
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
     room_number = models.ForeignKey(Rooms,on_delete= models.CASCADE)
     any_request = models.CharField(max_length=200)



