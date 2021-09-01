"""
Urls for the app product
"""
from django.urls import path
from .views import Products


urlpatterns = [
    # Endpoint all products
    path('products/', Products.as_view()),
]
