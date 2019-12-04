import logging

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from main.models import Order, CommentOrder, OrderPicture, Review, CommentReview
from main.serializers import OrderShortSerializer, OrderFullSerializer, OrderPictureSerializer, \
    CommentOrderShortSerializer, CommentOrderFullSerializer, ReviewShortSerializer, ReviewFullSerializer, \
    CommentReviewShortSerializer, CommentReviewFullSerializer, OrderPictureShortSerializer
from main.permissions import OrderPermission, CommentOrderPermission, CommentReviewPermission, ReviewPermission, \
    PictureOrderPermission, CommentInOrderPermission, PicturesInOrderPermission, CommentsInReviewPermission

logger = logging.getLogger(__name__)

@permission_classes((OrderPermission,))
@authentication_classes((JSONWebTokenAuthentication, ))
class OrderList(APIView):
    def get(self, request):
        try:
            orders = Order.objects.all()
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderShortSerializer(orders, many=True)

        return Response(serializer.data)

@permission_classes((OrderPermission,))
@authentication_classes((JSONWebTokenAuthentication, ))
class OrderCommentList(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        try:
            comments = CommentOrder.objects.filter(order_id=order.id)
        except CommentOrder.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentOrderShortSerializer(comments, many=True)

        return Response(serializer.data)

    
    def post(self, request, pk):
        instance = Order.objects.get(id=pk)
        serializer = CommentOrderFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, reciever=instance.customer, order=instance)
            logger.info(f"{self.request.user} added comment to order")
            return Response(serializer.data)
        return Response(serializer.errors)

@permission_classes((OrderPermission,))
@authentication_classes((JSONWebTokenAuthentication, ))
class OrderPictureList(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        try:
            pictures = OrderPicture.objects.filter(order_id=order.id)
        except OrderPicture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderPictureShortSerializer(pictures,
                                                many=True,
                                                context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, pk):
        instance = self.get_object()
        serializer = OrderPictureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=instance)
            logger.info(f"{self.request.user} added picture")
            return Response(serializer.data)
        return Response(serializer.errors)

@permission_classes((ReviewPermission,))
@authentication_classes((JSONWebTokenAuthentication, ))
class ReviewCommentList(APIView):
    def get(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        try:
            comments = CommentReview.objects.filter(order_id=review.id)
        except CommentReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentOrderShortSerializer(comments, many=True)

        return Response(serializer.data)

    
    def post(self, request, pk):
        instance = Review.objects.get(id=pk)
        serializer = CommentOrderFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, review=instance)
            logger.info(f"{self.request.user} added comment to review")
            return Response(serializer.data)
        return Response(serializer.errors)