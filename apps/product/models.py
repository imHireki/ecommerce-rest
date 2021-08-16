from django.db import models


class Product(models.Model):
    PRODUCT_TYPES = (
        ('S', 'Simple'),
        ('V', 'Variable'),
    )

    name = models.CharField(max_length=128)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    marketing_price = models.FloatField()
    marketing_price_promotional = models.FloatField(default=0)
    image = models.ImageField(
        upload_to="uploads/images/%Y/%m/",
        null=True,
        blank=True,
    )
    thumbnail = models.ImageField(
        upload_to="uploads/thumbnails/%Y/%m/",
        null=True,
        blank=True,
    )
    product_type = models.CharField(
        max_length=1,
        default='S',
        choices=PRODUCT_TYPES,
    )
    

class Variation(models.Model):
    CASCADE = models.CASCADE

    product = models.ForeignKey(
        to=Product,
        on_delete=CASCADE
    )
    name = models.CharField(max_length=128)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    inventory = models.PositiveIntegerField(default=0)
