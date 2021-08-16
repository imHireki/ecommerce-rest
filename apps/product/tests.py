from django.test import TestCase
from .models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(
            name='test',
            short_description='test',
            long_description='test',
            marketing_price=15,
        )        

    def test_product_creation(self):
        product = Product.objects.get(name='test')
        self.assertIsNotNone(
            product, msg='a' + str(product)
        )

        import sys
        sys.stdout.write(str(product.__dict__))
