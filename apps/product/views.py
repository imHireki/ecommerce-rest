"""
Products view for the ProductSerializer
"""
from django_filters.rest_framework.backends import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework import permissions

from .paginators import ProductListPagination
from .serializers import ProductSerializer
from .permissions import ReadOnly
from .filters import  PriceFilter
from .models import Product


class ProductCreateView(APIView):
    def post(self, *args, **kwargs):
        serializer = ProductSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    
class ProductListView(generics.ListCreateAPIView):
    # Content
    queryset = Product.objects.order_by(
        '-inventory'
    ).prefetch_related('images')
    serializer_class = ProductSerializer

    # Permissions
    permission_classes = [
        permissions.IsAdminUser | ReadOnly # Is admin or Read Only
    ]
    
    # Filters
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

    # Pagination
    pagination_class = ProductListPagination
