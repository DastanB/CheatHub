from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from users.models import MainUser, Profile
from utils.upload import user_avatar_delete_path


@receiver(post_save, sender=MainUser)
def user_created(sender, instance, created=True, **kwargs):
    if instance.first_name and instance.last_name and instance.full_name == '':
        instance.full_name = f'{instance.first_name} {instance.last_name}'
    if not instance.profile:
        Profile.objects.create(user=instance)


@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, created=True, **kwargs):
    user_avatar_delete_path(instance.avatar)


