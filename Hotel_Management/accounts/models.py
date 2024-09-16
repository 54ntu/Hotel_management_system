from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers  import CustomUserManager


# Create your models here.
class CustomUserModel(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('guest', 'Guest'),
    )
    email = models.EmailField(unique=True,max_length=50)
    phone_no = models.CharField(max_length=15)
    fullname = models.CharField(max_length= 50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    roles_choices = models.CharField(choices=ROLE_CHOICES,max_length=50)


    def __str__(self):
        return self.email



    USERNAME_FIELD= "email"
    REQUIRED_FIELDS =[]

    objects = CustomUserManager()