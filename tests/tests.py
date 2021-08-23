from apps.product.models import Product, ProductImage

from django.core.files.images import ImageFile, File
from django.test import TestCase
from django.conf import settings

from PIL import Image, ImageOps
from pathlib import Path
from io import BytesIO
from sys import stdout
import os


class ProductTestCase(TestCase):
    def setUp(self):
        img = self.create_test_image()
        self.product = Product.objects.create(
            name='test',
            price=15,
            # thumbnail=img
        )
        self.image_obj = ProductImage.objects.create(
            product=self.product,
            image=img
        )
        self.image_obj_2 = ProductImage.objects.create(
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
        product = self.product

        len_product_img = ProductImage.objects.filter(
            product__name=product
        ).count()

        self.resize_image(img_fp)

        if len_product_img != 1:
            return
        
        self.resize_thumbnail(img_fp)
        return

    @staticmethod
    def resize_image(img_fp):
        with Image.open(img_fp) as img_pil:
            LANCZOS = Image.LANCZOS
            new_sizes = (
                round(img_pil.width * 0.85),
                round(img_pil.height * 0.85),
            )
            resized_img_pil = img_pil.resize(
                size=new_sizes,
                resample=LANCZOS,
            )
            resized_img_pil.save(img_fp, optimize=True)
        return

    @staticmethod
    def resize_thumbnail(img_fp, img_name, product):
        NEW_THUMBNAIL_SIZE = (228, 228)
        ANTIALIAS = Image.ANTIALIAS

        with Image.open(img_fp) as img_pil:

            # Don't create a thumbnail if it already exists
            product = Product.objects.filter(
                name=product
            ).first()
            if product.thumbnail:
                stdout.write('THUMBNAIL EXISTS!')
                return img_pil

            # Managing names
            img_pil_name = Path(img_name).stem
            thumb_pil_name = f'{img_pil_name}_thumbnail.png'

            # Thumbnail file's modifications 
            thumbnail = img_pil.copy()
            thumbnail = ImageOps.pad(
                image=thumbnail, size=NEW_THUMBNAIL_SIZE,
                method=ANTIALIAS, color='white'
            )
            thumbnail_io = BytesIO()
            thumbnail.save(thumbnail_io, 'png', optimize=True)
            thumbnail_file = File(
                thumbnail_io, name=thumb_pil_name
            )
            
            # Saving thumbnail to Product
            product.thumbnail = thumbnail_file
            product.save()
            return
