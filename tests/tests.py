from django.test import TestCase
from apps.product.models import Product, Image
import sys


class ProductTestCase(TestCase):
    def setUp(self):
        product = Product.objects.create(
            name='test',
            price=15,
        )

        Image.objects.create(
            product=product,
            image='media/kagura.png'

        )
        
    def test_product_creation(self):
        product = Product.objects.get(name='test')
        image = Image.objects.get(product__name='test')

        self.assertIsNotNone(product)
        self.assertIsNotNone(image)

        sys.stdout.write(str(product.__dict__))
        sys.stdout.write('\n')
        sys.stdout.write(str(image.__dict__))
        sys.stdout.write(str())
    