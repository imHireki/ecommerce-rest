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
        # if self.image:
            # self.test_resizing_img_pillow()

    # def test_resizing_img_pillow(self):
    #     len_product_img = ProductImage.objects.filter(
    #         product__name=self.product
    #     ).count()

    #     img_fp = os.path.join(settings.MEDIA_ROOT, self.image.name)
        
    #     if len_product_img == 1:
    #         img_pil = Image.open(img_fp)

    #         img_pil.save(img_fp)

    #         # CREATING AND SAVING THUMBNAIL FILE
    #         NEW_SIZES = (228, 228)
    #         ANTIALIAS = Image.ANTIALIAS

    #         thumbnail = img_pil.copy()
    #         thumbnail = ImageOps.pad(
    #             image=thumbnail, size=NEW_SIZES,
    #             method=ANTIALIAS, color='white'
    #         )

    #         img_pil_name = Path(self.image.name).stem
    #         thumb_pil_name = f'{img_pil_name}-thumbnail.png'

    #         thumb_io = BytesIO()
    #         thumbnail.save(thumb_io, format='png', quality=85)
    #         thumbnail = File(thumb_io, name=thumb_pil_name)

    #         # ADDING THE THUMBNIAL TO THE PRODUCT
    #         product = Product.objects.filter(name=self.product).first()
    #         product.thumbnail = thumbnail
    #         product.save()

    #     return img_pil # retorno a original para o ProductImage
