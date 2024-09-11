from django.urls import path
from .views import  GuestRegistrationView,StaffRegistrationViewsets

urlpatterns = [
    path('guestRegister/',GuestRegistrationView.as_view({
        'post':'create'
    }),name='guest-register'),
     path('login/',GuestRegistrationView.as_view({
        'post':'login'
    }),name='guest-login'),
    path('staffRegistration/',StaffRegistrationViewsets.as_view({
        'post':'create'
    }),name='staff-register'),

]
