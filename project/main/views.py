from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.http import Http404
from django.shortcuts import get_object_or_404

from main import models, serializers

# Create your views here.
class OrderViewset(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderLongSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.OrderShortSerializer
        return serializers.OrderLongSerializer
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
        return serializer.data