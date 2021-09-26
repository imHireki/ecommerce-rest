"""
Paginators for the product app
"""
from rest_framework.pagination import PageNumberPagination


class ProductListPagination(PageNumberPagination):
    """ A PageNumberPagination that displays 6 products per page """
    page_size = 6
