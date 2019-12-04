from rest_framework import serializers
from main.models import Order, OrderPicture, CommentOrder, Review, CommentReview
from users.serializers import UserFullSerializer
from main.constants import ORDER_TYPES, PAYMENT_TYPES


class OrderShortSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField(read_only=True)
    executor_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'customer_name', 'executor_name', 'due_to', 'price')

    def get_customer_name(self, obj):
        if obj.customer:
            return obj.customer.full_name
        return ''

    def get_executor_name(self, obj):
        if obj.executor:
            return obj.executor.full_name
        return ''


class OrderFullSerializer(OrderShortSerializer):
    customer = UserFullSerializer(read_only=True)
    executor = UserFullSerializer(read_only=True)
    order_type_name = serializers.SerializerMethodField(read_only=True)
    payment_type_name = serializers.SerializerMethodField(read_only=True)

    class Meta(OrderShortSerializer.Meta):
        fields = OrderShortSerializer.Meta.fields + ('customer', 'executor', 'description', 'created_at',
                                                     'payment_type', 'payment_type_name', 'order_type',
                                                     'order_type_name')

    def get_payment_type_name(self, obj):
        types_dict = dict(PAYMENT_TYPES)
        if types_dict[obj.payment_type]:
            return types_dict[obj.payment_type]
        return ''

    def get_order_type_name(self, obj):
        types_dict = dict(ORDER_TYPES)
        if obj.order_type and types_dict[obj.order_type]:
            return types_dict[obj.order_type]
        return ''

    def validate_payment_type(self, value):
        if value < 1 or value > len(PAYMENT_TYPES) or not isinstance(value, int):
            raise serializers.ValidationError(f'Payment type options: {PAYMENT_TYPES}')
        return value

    def validate_order_type(self, value):
        if value < 1 or value > len(ORDER_TYPES) or not isinstance(value, int):
            raise serializers.ValidationError(f'Order type options: {ORDER_TYPES}')
        return value


class OrderPictureShortSerializer(serializers.Serializer):
    order_title = serializers.SerializerMethodField(read_only=True)
    file_full_path = serializers.SerializerMethodField(read_only=True)

    def get_order_title(self, obj):
        return obj.order.title

    def get_file_full_path(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)


class OrderPictureSerializer(serializers.Serializer):
    order = OrderFullSerializer(read_only=True)
    file = serializers.FileField()

    def create(self, validated_data):
        picture = OrderPicture(**validated_data)
        picture.save()
        return picture


class CommentOrderShortSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    reciever_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CommentOrder
        fields = ('id', 'user_name', 'reciever_name', 'message')

    def get_user_name(self, obj):
        return obj.user.full_name

    def get_reciever_name(self, obj):
        return obj.reciever.full_name


class CommentOrderFullSerializer(CommentOrderShortSerializer):
    order = OrderFullSerializer(read_only=True)
    user = UserFullSerializer(read_only=True)
    reciever = UserFullSerializer(read_only=True)

    class Meta(CommentOrderShortSerializer.Meta):
        fields = CommentOrderShortSerializer.Meta.fields + ('order', 'created_at', 'user', 'reciever')


class ReviewShortSerializer(serializers.ModelSerializer):
    user_name = UserFullSerializer(read_only=True)
    reciever_name = UserFullSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('user_name', 'reciever_name', 'rating')

    def get_user_name(self, obj):
        return obj.user.full_name

    def get_reciever_name(self, obj):
        return obj.reciever.full_name


class ReviewFullSerializer(ReviewShortSerializer):
    user = UserFullSerializer(read_only=True)
    reciever = UserFullSerializer(read_only=True)

    class Meta(ReviewShortSerializer.Meta):
        fields = ReviewShortSerializer.Meta.fields + ('user', 'reciever')

    def validate_rating(self, value):
        if not isinstance(value, int) and value < 1 or value > 5:
            serializers.ValidationError(f'Rating scale is from 1 to 5')
        return value


class CommentReviewShortSerializer(serializers.ModelSerializer):
    reciever_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CommentReview
        fields = ('id', 'reciever_name', 'message')

    def get_reciever_name(self, obj):
        return obj.reciever.full_name


class CommentReviewFullSerializer(CommentReviewShortSerializer):
    review = ReviewFullSerializer(read_only=True)
    user = UserFullSerializer(read_only=True)
    reciever = UserFullSerializer(read_only=True)

    class Meta(CommentReviewShortSerializer.Meta):
        fields = CommentReviewShortSerializer.Meta.fields + ('review', 'user', 'reciever', 'created_at')

    def create(self, validated_data):
        review_data = validated_data.get('review')
        Review.objects.create(**review_data)
        CommentReview.objects.create(**validated_data)
