from django.urls import path
from main.views import OrderViewset, CommentOrderViewSet, OrderPictureViewSet, ReviewViewset, CommentReviewViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('orders', OrderViewset, base_name='main')
router.register('ordercomments', CommentOrderViewSet, base_name='main')
router.register('orderpictures', OrderPictureViewSet, base_name='main')
router.register('reviews', ReviewViewset, base_name='main')
router.register('reviewcomments', CommentReviewViewSet, base_name='main')


urlpatterns = router.urls