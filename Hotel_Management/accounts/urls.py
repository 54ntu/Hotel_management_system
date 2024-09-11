from django.urls import path
from .views import  GuestRegistrationView

urlpatterns = [
    path('guestRegister/',GuestRegistrationView.as_view({
        'post':'create'
    }),name='guest-register'),
     path('guestLogin/',GuestRegistrationView.as_view({
        'post':'login'
    }),name='guest-login'),
]
