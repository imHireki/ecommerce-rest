from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.account import get_state_choices


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'cpf']
    USERNAME_FIELD = 'username'

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
    name = models.CharField(max_length=32)
    adress = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    complement = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=8)
    district = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(
        default='SP',
        max_length=2,
        choices = STATE_CHOICES,
    )

    class Meta:
        ordering = ('user',)
    
    def __str__(self):
        f"{self.user}'s {self.name} address"
