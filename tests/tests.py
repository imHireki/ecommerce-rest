from django.core.files.images import ImageFile
from django.test import TestCase

from io import BytesIO
from sys import stdout
from PIL import Image
import os

from apps.product.models import Product


class ProductTestCase(TestCase):
    def save_img(self, size, form, color='RGB'):
        img = Image.new(color, size)
        img.save(f'media/tests/{size}_{form}_{color}.{form}', form)
        img.close()

    def create_img(self):
        sizes = ((100, 50), (256, 256), (1280, 720))
        formats = ('png', 'jpeg')
        colors = ('RGBA', 'RGB')

        for s in range(len(sizes)):
            for f in range(len(formats)):
                if formats[f] == 'png':
                    for c in range(len(colors)):
                        self.save_img(sizes[s], formats[f], colors[c])
                else:
                    self.save_img(sizes[s], formats[f])

    def get_img_file(self, name, form):
        with Image.open(f'media/tests/{name}') as image:
            img_io = BytesIO()
            image.save(img_io, format=form)
            image_file = ImageFile(img_io, name=name)
        return image_file

    def test_resize_image(self):
        self.test_images = [name for name in os.listdir('media/tests/')]

        for img_name in self.test_images:
            img_file = self.get_img_file(img_name, 'png')

            product = Product.objects.create(
                name=img_name, price=15, thumbnail=img_file
            )
            thumb = Product.objects.get(name=img_name).thumbnail

            self.img_size = (thumb.width, thumb.height)
            self.img_ext = os.path.splitext(thumb.name)[1]
            self.img_name = thumb.name
        
            self.assertIn('_Cmprssd', self.img_name)
            self.assertLessEqual(self.img_size[0], 256)
            self.assertEqual(self.img_ext, '.jpg')
    