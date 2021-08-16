from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    PRODUCT_TYPES = (
        ('S', 'Simple'),
        ('V', 'Variable'),
    )

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Placed after first save to get self.id
        if not self.slug:
            self.slug = self.auto_slug(self.pk, self.name)
            self.save()

    @staticmethod
    def auto_slug(pk, name):
        """ Creates a Slug with the user id/pk at the end """
        dash_id = f'-{pk}'
        return slugify(name) + dash_id


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
