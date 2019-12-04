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

@api_view(['GET'])
@permission_classes((OrderPermission,))
@authentication_classes((JSONWebTokenAuthentication, ))
def orders(request):
    try:
        orders = Order.objects.all()
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = OrderShortSerializer(orders, many=True)

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((OrderPermission,))
@authentication_classes((JSONWebTokenAuthentication, ))
def orderpics(request, pk):
    order = get_object_or_404(Order, id=pk)
    try:
        pictures = OrderPicture.objects.filter(order_id=order.id)
    except OrderPicture.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = OrderPictureShortSerializer(pictures,
                                            many=True,
                                            context={'request': request})
    return Response(serializer.data)