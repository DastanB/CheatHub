from django.db import models
from django.db.models import Q
from users.models import MainUser
from main.constants import *
from utils import *
from main.constants import *

from datetime import datetime


class OrderManager(models.Manager):
    def get_active(self):
        return self.filter(due_to__gte=datetime.now())

    def get_expired(self):
        return self.filter(due_to__lte=datetime.now())

    def get_essays(self):
        return self.filter(status=ORDER_ESSAY)

    def get_math_problems(self):
        return self.filter(status=ORDER_MATH)

    def get_it_projects(self):
        return self.filter(status=ORDER_IT_PROJECT)

    def get_done_cash(self):
        return self.filter(Q(due_to__lte=datetime.now()) & Q(payment_type=PAYMENT_VIA_CASH))

    def get_done_card(self):
        return self.filter(Q(due_to__lte=datetime.now()) & Q(payment_type=PAYMENT_VIA_CARD))


class Order(models.Model):
    customer = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_orders')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='todo_tasks', null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now=True)
    due_to = models.DateTimeField()
    price = models.PositiveIntegerField()
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPES, default=PAYMENT_VIA_CASH)
    order_type = models.PositiveSmallIntegerField(choices=ORDER_TYPES, null=True)

    objects = OrderManager()

    def __str__(self):
        return self.title

class OrderPictureManager(models.Manager):
    def get_pics_of_order(self, order):
        return self.filter(order=order)

 
class OrderPicture(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pictures')
    file = models.FileField(upload_to=order_document_path, validators=[validate_file_size, validate_extension],
                                null=True, blank=True)
    objects = OrderPictureManager()

    def __str__(self):
        return self.order.title

class Comment(models.Model):
    message = models.CharField(max_length=10000000)
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_comments')

class CommentOrderManager(models.Manager):
    def get_comments_of_order(self, order):
        return self.filter(order=order)

class CommentOrder(Comment):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comments')
    reciever = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='comments_to_me', null=True)

    objects = CommentOrderManager()

    def __str__(self):
        return self.order.title


class ReviewManager(models.Manager):
    def get_by_rating(self, rating):
        if isinstance(rating, int) and rating >= 1 and rating <= 5:
            return self.filter(rating=rating)
        raise ValidationError


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Review(models.Model):
    rating = IntegerRangeField(min_value=1, max_value=5)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_reviews')
    reciever = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='reviews_to_me', null=True)

    def __str__(self):
        return self.reciever.username


class CommentReview(Comment):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)

    def __str__(self):
        return self.review.reciever.username