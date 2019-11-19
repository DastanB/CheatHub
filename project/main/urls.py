from django.urls import path
from main.views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('orders', OrderViewset, base_name='main')

urlpatterns = router.urls