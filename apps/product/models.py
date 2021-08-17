from django.db import models
from utils.product import auto_slug


""" TODO: ADD A CATEGORY MODEL """

CASCADE = models.CASCADE


class Product(models.Model):
    PRODUCT_TYPES = (
        ('S', 'Simple'),
        ('V', 'Variable'),
    )

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    price = models.FloatField()
    price_off = models.FloatField(default=0)
    inventory = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(
        upload_to="uploads/thumbnails/%Y/%m/",
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Placed after first save to get self.id
        if not self.slug:
            self.slug = auto_slug(self.pk, self.name)
            self.save()
    

class Image(models.Model):
    """ Many images for one product """
    product = models.ForeignKey(
        to=Product,
        on_delete=CASCADE
    )
    image = models.ImageField(
        upload_to="uploads/images/%Y/%m/",
        blank=True,
        null=True,
    )
