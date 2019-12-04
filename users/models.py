from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from utils.upload import user_avatar_path
from utils.validators import validate_file_size, validate_extension


class University(models.Model):
    name = models.CharField(max_length=100)


class MainUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class MainUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    full_name = models.CharField(max_length=181, blank=True)
    is_customer = models.BooleanField(default=False)
    is_executor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MainUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500)
    avatar = models.FileField(upload_to=user_avatar_path, validators=[validate_file_size, validate_extension],
                              null=True, blank=True)
    university = models.ForeignKey(University, on_delete=models.SET(None), null=True)

    def __str__(self):
        return self.user.username


class ActivationManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class Activation(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='activation')
    is_active = models.BooleanField(default=True)

    objects = ActivationManager()