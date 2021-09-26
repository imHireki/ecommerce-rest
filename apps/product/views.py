"""
Products view for the ProductSerializer
"""
from django_filters.rest_framework.backends import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework.views import APIView

from .paginators import ProductListPagination
from .serializers import ProductSerializer
from .filters import  PriceFilter
from .models import Product


class ProductCreateView(APIView):
    def post(self, *args, **kwargs):
        serializer = ProductSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    
class ProductListView(generics.ListCreateAPIView):
    # List content
    queryset = Product.objects.order_by(
        '-inventory'
    ).prefetch_related('images')
    serializer_class = ProductSerializer
    
    # List filters
    filter_backends = (
        # drf filters
        filters.SearchFilter,
        filters.OrderingFilter,

        # django-filter lib
        DjangoFilterBackend,
    )
    filterset_class = PriceFilter
    search_fields = ['name', 'description',]
    ordering_fields = ['name', 'description', 'price_off']

    pagination_class = ProductListPagination
