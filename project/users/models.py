from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MainUser(AbstractUser):
    is_creator = models.BooleanField(default=False)
    is_executor = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        # return '%s %s' % (self.id, self.user)
        #
        # return '{0}: {1}'.format(self.id, self.username)
        return f'{self.id}: {self.username}'

class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    address = models.CharField(max_length=300)
    avatar = models.FileField()

    def __str__(self):
        return self.user.username