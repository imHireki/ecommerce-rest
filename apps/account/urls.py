"""
URLs mapping for the account management
provided by Djoser
"""
from django.urls import path, include


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
