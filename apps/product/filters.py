"""
App product filters
    - PriceFilter
"""
from django_filters.rest_framework import FilterSet, filters

from .models import Product


class PriceFilter(FilterSet):
    """ Filter that makes a price range search """
    price_range = filters.RangeFilter(
        field_name='price_off',
        label='Price Range'
    )

    class Meta:
        model = Product
        fields = ('price_range',)
