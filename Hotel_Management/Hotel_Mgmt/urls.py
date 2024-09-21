from django.urls  import path,include
from rest_framework.routers   import DefaultRouter

from .views import CategoryViewsets,FeedBackViewsets,InventoryViewsets,SupplierInfoViewset,StaffManagementViewsets,RoomViewsets,RoomAvailabilityViewsets,RoomBookingViesets,CancelBookingViewsets,InvoiceViewsets


router = DefaultRouter()

router.register(r'category',CategoryViewsets)
router.register(r'feedback',FeedBackViewsets)  #here guest or anyone who is logged in can give his/her feedback about the Hotel or restaurant
router.register(r'inventory',InventoryViewsets)
router.register(r'supplier',SupplierInfoViewset)
router.register(r'staff', StaffManagementViewsets)
router.register(r'rooms',RoomViewsets)
router.register(r'room-available',RoomAvailabilityViewsets,basename='room-available')
router.register(r'roombookings',RoomBookingViesets)
router.register(r'cancelBooking',CancelBookingViewsets ,basename='cancel-booking')
router.register(r'invoice',InvoiceViewsets)



urlpatterns = [
    path('',include(router.urls))
]
