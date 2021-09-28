"""
Products view for the ProductSerializer
"""
from django_filters.rest_framework.backends import DjangoFilterBackend

from rest_framework import generics, filters
from rest_framework import permissions

from .paginators import ProductListPagination
from .serializers import ProductSerializer
from .permissions import ReadOnly
from .filters import  PriceFilter
from .models import Product


class ProductListView(generics.ListCreateAPIView):
    """ 
    View for the product list

    Return a response a list of product's objects
        - ordering = descending `inventory`
        - permissions = is admin or read only
        - filters = search, ordering and price range
        - pagination = Page number with 6 products per page
    """
    
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
