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
            thumbnail=img
        )
        self.image_obj = ProductImage.objects.create(
            product=self.product,
            image=img
        )

    def test_product_creation(self):
        self.assertIsNotNone(self.product)
        self.assertIsNotNone(self.image)
        
    @staticmethod
    def create_test_image():
        img_name = 'luffy.jpeg'
        with Image.open(f'media/{img_name}') as image:
            img_io = BytesIO()
            image.save(img_io, format='jpeg')
            image_file = ImageFile(img_io, name=img_name)
        return image_file

    def test_resize_thumbnail(self):
        product = Product.objects.get(name='test')
        thumb = product.thumbnail

        thumb_size = (thumb.width, thumb.height)
        thumb_ext = os.path.splitext(thumb.name)[1]
        thumb_name = thumb.name

        self.assertIn('_Cmprssd', thumb_name)
        self.assertLessEqual(thumb_size[0], 256)
        self.assertEqual(thumb_ext, '.jpg')
    

    def test_resize_image(self):
        image = ProductImage.objects.get(
            product__name=self.product
        ).image

        img_size = (image.width, image.height)
        img_ext = os.path.splitext(image.name)[1]
        img_name = image.name

        self.assertIn('_Cmprssd', img_name)
        self.assertLessEqual(img_size[0], 800)
        self.assertEqual(img_ext, '.jpg')
