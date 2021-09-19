"""
App product tests
"""
from django.test import TestCase
import os

from .utils import get_img_file, create_img
from apps.product.models import Product


class ProductTestCase(TestCase):

    def test_resize_image(self):
        """ 
        Test if the test images are `compressed`, `resized` and in `.jpg` format
        """
        try:
            os.mkdir('media/tests/')
        except OSError:
            pass
        
        create_img() if not len(os.listdir('media/tests/')) else None

        test_images = [name for name in os.listdir('media/tests/')]

        for img_name in test_images:
            img_file = get_img_file(img_name, 'png')

            Product.objects.create(name=img_name, price=15, thumbnail=img_file)
            thumb = Product.objects.get(name=img_name).thumbnail

            self.img_size = (thumb.width, thumb.height)
            self.img_ext = os.path.splitext(thumb.name)[1]
            self.img_name = thumb.name
        
            self.assertIn('_Cmprssd', self.img_name)
            self.assertLessEqual(self.img_size[0], 256)
            self.assertEqual(self.img_ext, '.jpg')
