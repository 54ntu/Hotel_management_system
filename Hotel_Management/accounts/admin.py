from django.contrib import admin
from .models import CustomUserModel

# Register your models here.

@admin.register(CustomUserModel)
class CustomUserAdminModel(admin.ModelAdmin):
    list_display = ('id','email','username','phone_no','fullname','city','roles_choices','is_active','is_superuser','is_staff')
