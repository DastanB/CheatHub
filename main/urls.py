from django.urls import path
from main.views import OrderViewset, CommentOrderViewSet, OrderPictureViewSet, ReviewViewset, CommentReviewViewSet, OrderCommentList, OrderList, OrderPictureList, ReviewCommentList, orders, orderpics
from rest_framework import routers

urlpatterns = [
    # path('orders', OrderList.as_view()),
    # path('orders/<int:pk>/comments', OrderCommentList.as_view()),
    # path('orders/<int:pk>/pics', OrderPictureList.as_view()),
    # path('review/<int:pk>/comments', ReviewCommentList.as_view()), 
    # path('orders', orders),
    # path('orders/<int:pk>/pics', orderpics),
    
]

router = routers.DefaultRouter()
router.register('orders', OrderViewset, base_name='main')
router.register('ordercomments', CommentOrderViewSet, base_name='main')
router.register('orderpictures', OrderPictureViewSet, base_name='main')
router.register('reviews', ReviewViewset, base_name='main')
router.register('reviewcomments', CommentReviewViewSet, base_name='main')


urlpatterns += router.urls