"""
Products view for the ProductSerializer
"""

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductSerializer
from .models import Product


class Products(APIView):
    """ Get the Product and its images """
    def get(self, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
