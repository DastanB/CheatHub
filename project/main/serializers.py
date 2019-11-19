from rest_framework import serializers
from main.models import Order

class OrderShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'description', 'price', 'due_to', 'order_type')

class OrderLongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'