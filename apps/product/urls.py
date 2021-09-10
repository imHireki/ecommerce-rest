"""
Urls for the app product
"""
from django.urls import path
from .views import Products


urlpatterns = [
    path('products/', Products.as_view()),
]
