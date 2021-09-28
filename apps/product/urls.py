"""
Urls for the app product
"""
from django.urls import path

from .views import ProductListView


urlpatterns = [
    path('products/', ProductListView.as_view()),
]
