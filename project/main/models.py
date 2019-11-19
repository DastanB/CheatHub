from django.db import models
from users.models import MainUser
from main.constants import *
from utils import *

from datetime import datetime

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='my_orders')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='todo_tasks', null=True)
    description = models.CharField(max_length=10000)
    pictures = models.FileField(upload_to=order_document_path, validators=[validate_file_size, validate_extension],
                                null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    due_to = models.DateTimeField()
    price = models.PositiveIntegerField()
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPES, default=PAYMENT_VIA_CASH)
    order_type = models.PositiveSmallIntegerField(choices=ORDER_TYPES, null=True)