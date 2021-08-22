from django.conf import settings
from django.core.files import File
from django.db import models

from PIL import Image, ImageOps
from pathlib import Path
from io import BytesIO
import os

from utils.product import auto_slug


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
        upload_to='uploads/thumbnails/%Y/%m/', blank=True, null=True,
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Placed after first save to get self.id
        if not self.slug:
            self.slug = auto_slug(self.pk, self.name)
            self.save()
            

class ProductImage(models.Model):
    """ Many images for one product """
    CASCADE = models.CASCADE

    product = models.ForeignKey(
        to=Product,
        on_delete=CASCADE
    )
    image = models.FileField(
        upload_to="uploads/images/%Y/%m/",
    )

    def __str__(self):
        # TODO: FIX STR
        return f'image {self.pk} from {self.product}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_img()

    def resize_img(self):
        img_name = self.image.name
        img_fp = os.path.join(settings.MEDIA_ROOT, img_name)

        len_product_img = ProductImage.objects.filter(
            product__name=self.product
        ).count()

        if len_product_img == 1:
            NEW_SIZES = (228, 228)
            ANTIALIAS = Image.ANTIALIAS

            with Image.open(img_fp) as img_pil:
                # Don't create a thumbnail if it already exists
                product = Product.objects.filter(
                    name=self.product
                ).first()

                if product.thumbnail:
                    print('thumbnail exists!')
                    return img_pil

                # Managing names
                img_pil_name = Path(img_name).stem
                thumb_pil_name = f'{img_pil_name}_thumbnail.png'

                # Thumbnail file's modifications 
                thumbnail = img_pil.copy()
                thumbnail = ImageOps.pad(
                    image=thumbnail, size=NEW_SIZES,
                    method=ANTIALIAS, color='white'
                )
                thumbnail_io = BytesIO()
                thumbnail.save(thumbnail_io, 'png')
                thumbnail_file = File(
                    thumbnail_io, name=thumb_pil_name
                )
                
                # Saving thumbnail to Product
                product.thumbnail = thumbnail_file
                product.save()

        return img_pil
