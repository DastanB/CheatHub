from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from django.shortcuts import get_object_or_404

from main.models import Order, CommentOrder, OrderPicture, Review, CommentReview
from main.serializers import OrderShortSerializer, OrderFullSerializer, OrderPictureSerializer, \
    CommentOrderShortSerializer, CommentOrderFullSerializer, ReviewShortSerializer, ReviewFullSerializer, \
    CommentReviewShortSerializer, CommentReviewFullSerializer, OrderPictureShortSerializer
from main.permissions import OrderPermission, CommentOrderPermission, CommentReviewPermission, ReviewPermission, \
    PictureOrderPermission, CommentInOrderPermission, PicturesInOrderPermission, CommentsInReviewPermission


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (OrderPermission,)
    parser_classes = (FormParser, MultiPartParser, JSONParser,)

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderShortSerializer
        return OrderFullSerializer
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
        return serializer.data
    
    @action(methods=['GET', 'POST'], detail=True, permission_classes=[CommentInOrderPermission])
    def comments(self, request, pk):
        if request.method == 'GET':
            order = get_object_or_404(Order, id=pk)
            try:
                comments = CommentOrder.objects.filter(order_id=order.id)
            except CommentOrder.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CommentOrderShortSerializer(comments, many=True)

            return Response(serializer.data)
        
        if request.method == 'POST':
            instance = self.get_object()
            serializer = CommentOrderFullSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=self.request.user, reciever=instance.customer, order=instance)
                return Response(serializer.data)
            return Response(serializer.errors)
    
    @action(methods=['GET', 'POST'], detail=True, permission_classes=[PicturesInOrderPermission])
    def pictures(self, request, pk):
        if request.method == 'GET':
            order = get_object_or_404(Order, id=pk)
            try:
                pictures = OrderPicture.objects.filter(order_id=order.id)
            except OrderPicture.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = OrderPictureShortSerializer(pictures,
                                                   many=True,
                                                   context={'request': request})
            return Response(serializer.data)
        
        if request.method == 'POST':
            instance = self.get_object()
            serializer = OrderPictureSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(order=instance)
                return Response(serializer.data)
            return Response(serializer.errors)


class CommentOrderViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = CommentOrder.objects.all()
    serializer_class = CommentOrderFullSerializer
    permission_classes = (CommentOrderPermission,)


class OrderPictureViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = OrderPicture.objects.all()
    permission_classes = (PictureOrderPermission,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderPictureSerializer
        return OrderPictureSerializer


class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = (ReviewPermission,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewShortSerializer
        return ReviewFullSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data
    
    @action(methods=['GET', 'POST'], detail=True, permission_classes=[CommentsInReviewPermission])
    def comments(self, request, pk):
        if request.method is 'GET':
            review = get_object_or_404(Review, id=pk)
            try:
                comments = CommentReview.objects.filter(review_id=review.id)
            except CommentReview.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CommentReviewShortSerializer(comments, many=True)

            return Response(serializer.data)
        
        if request.method == 'POST':
            instance = self.get_object()
            serializer = CommentOrderFullSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=self.request.user, review=instance)
                return Response(serializer.data)
            return Response(serializer.errors)


class CommentReviewViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = CommentReview.objects.all()
    serializer_class = CommentReviewFullSerializer
    permission_classes = (CommentReviewPermission,)