from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import get_state_choices


class User(AbstractUser):
    REQUIRED_FIELDS = ['email',]
    USERNAME_FIELD = 'username'

    email = models.EmailField(max_length=255, unique=True)
    cpf = models.CharField(max_length=11, null=True)
    birth_date = models.DateField(null=True)

    class Meta:
        ordering = ('username',)
    
    def __str__(self):
        return self.username


class UserAddress(models.Model):
    STATE_CHOICES = get_state_choices()
    CASCADE = models.CASCADE

    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=16)
    adress = models.CharField(max_length=64)
    number = models.CharField(max_length=8)
    complement = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=8)
    district = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    state = models.CharField(
        default='SP',
        max_length=2,
        choices = STATE_CHOICES,
    )

    class Meta:
        ordering = ('user',)
    
    def __str__(self):
        f"{self.user}'s {self.name} address"
