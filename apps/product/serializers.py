from rest_framework.serializers import ModelSerializer
from .models import Product, ProductImage


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image',)

class ProductSerializer(ModelSerializer):
    
    # Images require related_name='images' on FK
    images = ProductImageSerializer(many=True)
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description',
            'slug', 'price', 'price_off',
            'inventory', 'thumbnail', 'images',
        )
        