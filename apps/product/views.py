from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ProductSerializer
from .models import Product


class Products(APIView):
    def get(self, args_kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    