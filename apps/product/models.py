"""
Product and ProductImage models
"""
from django.db import models

from .utils import auto_slug, resize


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
    price_off = models.FloatField(blank=True, null=True)
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

        # Set the price_off the same value as the price
        if not self.price_off:
            self.price_off = self.price
    
        super().save(*args, **kwargs)
        need_resave = False

        # Resize thumbnail
        if self.thumbnail and POS_RESIZE_STR not in self.thumbnail.name:
            self.thumbnail = resize(self.thumbnail, (256, 256))
            need_resave = True

        # Make an URL slug
        if not self.slug:
            self.slug = auto_slug(self.pk, self.name)
            need_resave = True

        if need_resave:
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
