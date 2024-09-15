from django.urls  import path,include
from rest_framework.routers   import DefaultRouter

from .views import CategoryViewsets,FeedBackViewsets


router = DefaultRouter()

router.register(r'category',CategoryViewsets)
router.register(r'feedback',FeedBackViewsets)  #here guest or anyone who is logged in can give his/her feedback about the Hotel or restaurant



urlpatterns = [
    path('',include(router.urls))
]
