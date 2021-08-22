from apps.product.models import Product, ProductImage

from django.core.files.images import ImageFile
from django.core.files import File
from django.test import TestCase
from django.conf import settings

from PIL import Image, ImageOps
from pathlib import Path
from io import BytesIO
from sys import stdout
import os


class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='test',
            price=15,
        )

        img = self.create_test_image()
        self.image_obj = ProductImage.objects.create(
            product=self.product,
            image=img
        )

    def test_product_creation(self):
        # Testing query's objects
        self.assertIsNotNone(self.product)
        self.assertIsNotNone(self.image)
        
    @staticmethod
    def create_test_image():
        with Image.open('media/py.png') as image:
            img_io = BytesIO()
            image.save(img_io, format='png')
            image_file = ImageFile(img_io, name='test.png')

        return image_file
        
    def test_resizing_img_pillow(self):
        img_name = self.image_obj.image.name
        img_fp = os.path.join(settings.MEDIA_ROOT, img_name)

        len_product_img = ProductImage.objects.filter(
            product__name=self.product
        ).count()

        if len_product_img == 1:
            NEW_SIZES = (228, 228)
            ANTIALIAS = Image.ANTIALIAS

            with Image.open(img_fp) as img_pil:  
                thumbnail = img_pil.copy()

                # Managing names
                img_pil_name = Path(img_name).stem
                thumb_pil_name = f'{img_pil_name}_thumbnail.png'

                # Thumbnail file's modifications 
                thumbnail = ImageOps.pad(
                    image=thumbnail, size=NEW_SIZES,
                    method=ANTIALIAS, color='white'
                )
                thumbnail_io = BytesIO()
                thumbnail.save(thumbnail_io, 'png')
                thumbnail_file = File(thumbnail_io, name=thumb_pil_name)

                # Saving thumbnail to Product
                product = Product.objects.filter(name=self.product).first()
                product.thumbnail = thumbnail_file
                product.save()

        return img_pil
