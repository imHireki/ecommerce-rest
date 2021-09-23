"""
Urls for the app product
"""
from django.urls import path

from .views import ProductCreateView, ProductListView


urlpatterns = [
    path('', ProductCreateView.as_view()),
    path('products/', ProductListView.as_view()),
]
