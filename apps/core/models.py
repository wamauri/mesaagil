from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
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


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='E-mail', 
        validators=[validate_email],
        unique=True
    )
    full_name = models.CharField(
        verbose_name='Full Name', 
        max_length=255
    )
    is_waiter = models.BooleanField(
        verbose_name='Is waiter?',
        default=False,
        null=True,
        blank=True
    )
    is_client = models.BooleanField(
        verbose_name='Is client?',
        default=False,
        null=True,
        blank=True
    )
    username = models.CharField(
        max_length=100, 
        unique=False, 
        null=True,
        blank=True,
        default=''   
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self) -> str:
        return self.email
