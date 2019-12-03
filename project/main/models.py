from django.db import models
from users.models import MainUser
from main.constants import *
from utils import *

from datetime import datetime

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_orders')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='todo_tasks', null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField(default=datetime.now)
    due_to = models.DateTimeField()
    price = models.PositiveIntegerField()
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPES, default=PAYMENT_VIA_CASH)
    order_type = models.PositiveSmallIntegerField(choices=ORDER_TYPES, null=True)

    def __str__(self):
        return self.title

class OrderPicture(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pictures')
    file = models.FileField(upload_to=order_document_path, validators=[validate_file_size, validate_extension],
                                null=True, blank=True)
    
    def __str__(self):
        return self.order.title

class CommentOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments')
    message = models.CharField(max_length=10000000)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_comments')
    reciever = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='comments_to_me', null=True)

    def __str__(self):
        return self.order.title

class Review(models.Model):
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_reviews')
    reciever = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='reviews_to_me', null=True)

    def __str__(self):
        return self.reciever.username

class CommentReview(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    message = models.CharField(max_length=10000000)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_comment_to_reviews')

    def __str__(self):
        return self.review.reciever.username