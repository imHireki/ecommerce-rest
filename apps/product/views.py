"""
Products view for the ProductSerializer
"""
from django_filters.rest_framework.backends import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters

from .serializers import ProductSerializer
from .filters import  PriceFilter
from .models import Product


class ProductCreateView(APIView):
    def post(self, *args, **kwargs):
        serializer = ProductSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().prefetch_related('images')
    serializer_class = ProductSerializer
    search_fields = ('name', 'description',)
    filterset_class = PriceFilter
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,)
