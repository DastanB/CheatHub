from django.db.models.signals import post_delete
from django.dispatch import receiver

from main.models import OrderPicture, Order
from utils.upload import order_delete_path, order_picture_delete_path


@receiver(post_delete, sender=OrderPicture)
def order_deleted(sender, instance, created=True, **kwargs):
    order_delete_path(instance)


@receiver(post_delete, sender=OrderPicture)
def order_picture_deleted(sender, instance, created=True, **kwargs):
    order_picture_delete_path(instance.file)


