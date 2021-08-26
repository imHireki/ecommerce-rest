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

    def test_product_creation(self):
        self.assertIsNotNone(self.product)
        self.assertIsNotNone(self.image)
        
    @staticmethod
    def create_test_image():
        with Image.open('media/py.png') as image:
            img_io = BytesIO()
            image.save(img_io, format='png')
            image_file = ImageFile(img_io, name='test.png')
        return image_file
