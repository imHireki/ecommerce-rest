from django.contrib.auth.models import AbstractUser
from django.db import models


CASCADE = models.CASCADE
STATE_CHOICES =  (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)

class User(AbstractUser):
    """
    cpf, birth_date
    """
    cpf = models.CharField(max_length=11, null=True)
    birth_date = models.DateField(null=True)

    REQUIRED_FIELDS = ['cpf', 'email',]
    
    def __str__(self):
        return self.username
    

class UserAddress(models.Model):
    """ Many adresses for each user """
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

    def __str__(self):
        f"{self.user}'s {self.name} address"
    