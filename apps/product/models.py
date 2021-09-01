"""
Product and ProductImage models
"""
from django.db import models

from utils.product import auto_slug, resize


POS_RESIZE_STR = '_Cmprssd'

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
        upload_to='uploads/thumbnails/%Y/%m/',
        blank=True, null=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        needs_resave = False

        if self.thumbnail and POS_RESIZE_STR not in self.thumbnail.name:
            self.thumbnail = resize(self.thumbnail, (256, 256))
            needs_resave = True

        if not self.slug:
            self.slug = auto_slug(self.pk, self.name)
            needs_resave = True
        
        if needs_resave:
            self.save()


class ProductImage(models.Model):
    """ Many images for one product """
    CASCADE = models.CASCADE

    product = models.ForeignKey(
        to=Product,
        on_delete=CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        upload_to="uploads/images/%Y/%m/",
    )

    def __str__(self):
        return f'image from product {self.product}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and POS_RESIZE_STR not in self.image.name:
            self.image = resize(self.image, (800, 800))
            self.save()
