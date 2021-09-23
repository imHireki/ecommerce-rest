"""
Serializers for the product app's models

ProductImageSerializer -> ProductImage
ProductSerializer      -> Product
"""
from rest_framework.serializers import ModelSerializer
from .models import Product, ProductImage


class ProductImageSerializer(ModelSerializer):
    """ Serializer for the ProductImage model """
    class Meta:
        model = ProductImage
        fields = ('id', 'image',)

class ProductSerializer(ModelSerializer):
    """ Serializer for the Product Model """

    # Images require related_name='images' on FK
    images = ProductImageSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'slug',
            'price', 'price_off', 'inventory',
            'thumbnail', 'images',
        )
