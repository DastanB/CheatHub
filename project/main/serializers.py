from rest_framework import serializers
from main.models import Order, OrderPicture, CommentOrder, Review, CommentReview
from users.serializers import UserSerializer
class OrderShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'description', 'price', 'due_to', 'order_type')

class OrderLongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderPictureSerializer(serializers.ModelSerializer):
    order = OrderShortSerializer(read_only=True)
    class Meta:
        model = OrderPicture
        fields = '__all__'

class CommentOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    reciever = UserSerializer()
    class Meta:
        model = CommentOrder
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    reciever = UserSerializer()
    class Meta:
        model = Review
        fields = '__all__'

class CommentReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = CommentReview
        fields = '__all__'

