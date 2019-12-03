from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from django.shortcuts import get_object_or_404

from main.models import Order, CommentOrder, OrderPicture, Review, CommentReview
from main.serializers import OrderLongSerializer, OrderShortSerializer, OrderPictureSerializer, CommentOrderSerializer, ReviewSerializer, CommentReviewSerializer

# Create your views here.
class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderLongSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderShortSerializer
        return OrderLongSerializer
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
        return serializer.data
    
    @action(methods=['GET', 'POST'], detail=True)
    def comments(self, request, pk):
        if request.method is 'GET':
            order = get_object_or_404(Order, id=pk)
            comments = CommentOrderSerializer(CommentOrder.objects.get(order_id=order.id), many=True)

            return Response(comments.data)
        
        if request.method == 'POST':
            instance = self.get_object()
            request.data['order'] = instance.id
            serializer = CommentOrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data)
            return Response(serializer.errors)
    
    @action(methods=['GET', 'POST'], detail=True)
    def pictures(self, request, pk):
        if request.method is 'GET':
            order = get_object_or_404(Order, id=pk)
            pictures = OrderPictureSerializer(OrderPicture.objects.get(order_id=order.id), many=True)

            return Response(pictures.data)
        
        if request.method == 'POST':
            instance = self.get_object()
            request.data['order'] = instance.id
            serializer = CommentOrderSerializer(data=request.data)
            if serializer.is_valid():
                if instance.customer.id == request.user:
                    serializer.save()
                    return Response(serializer.data)
            return Response(serializer.errors)

class CommentOrderViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = CommentOrder.objects.all()
    serializer_class = CommentOrderSerializer
    permission_classes = (IsAuthenticated,)

class OrderPictureViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = OrderPicture.objects.all()
    serializer_class = OrderPictureSerializer
    permission_classes = (IsAuthenticated,)

class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = CommentReviewSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return serializer.data
    
    @action(methods=['GET', 'POST'], detail=True)
    def comments(self, request, pk):
        if request.method is 'GET':
            review = get_object_or_404(Review, id=pk)
            comments = CommentReviewSerializer(CommentReview.objects.get(review_id=review.id), many=True)

            return Response(comments.data)
        
        if request.method == 'POST':
            instance = self.get_object()
            request.data['review'] = instance.id
            serializer = CommentOrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data)
            return Response(serializer.errors)

class CommentReviewViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = CommentReview.objects.all()
    serializer_class = CommentReviewSerializer
    permission_classes = (IsAuthenticated,)