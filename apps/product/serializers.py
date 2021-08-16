from rest_framework.serializers import ModelSerializer
from .models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'slug',
            'marketing_price', 'marketing_price_promotional',
            'image', 'thumbnail', 'product_type',
        ] 
