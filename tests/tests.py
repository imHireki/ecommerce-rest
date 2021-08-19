from apps.product.models import Product, Image

from django.core.files.images import ImageFile
from django.test import TestCase
from django.conf import settings

from io import BytesIO
from sys import stdout
from PIL import Image as Img, ImageOps, ImageFilter


class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='test',
            price=15,
        )

        img = self.create_test_image()

        self.image_obj = Image.objects.create(
            product=self.product,
            image=img
        )
        self.image_obj_2 = Image.objects.create(
            product=self.product,
            image=img
        )

    def test_product_creation(self):
        # Testing query's objects
        self.assertIsNotNone(self.product)
        self.assertIsNotNone(self.image)

        # Checking the object's attributes
        stdout.write(str(self.product.__dict__))
        stdout.write('\n')
        stdout.write(str(self.image.__dict__))
        
    @staticmethod
    def create_test_image():
        image = Img.open('media/py.png')
        # image = Img.new('RGBA', size=(50,50), color=(256,0,0))
        image_file = BytesIO()
        image.save(image_file, 'PNG')
        file = ImageFile(image_file, name='test.png')
        return file

    def test_resizing_img_pillow(self):
        len_product_img = Image.objects.filter(
            product__name=self.product
        ).count()

        image_fp = str(settings.MEDIA_ROOT) + self.image_obj.image.name
        img_pil = Img.open(image_fp)

        if len_product_img > 1:
            new_sizes = (228, 228)
            ANTIALIAS = Img.ANTIALIAS

            img_pil = Img.open(image_fp)

            # TODO: add blur mirrored padding/border
            pad_img = ImageOps.pad(
                image=img_pil,
                size=new_sizes,
                method=ANTIALIAS,
                color='white'
            )
            pad_img.save(image_fp)
            return
        
