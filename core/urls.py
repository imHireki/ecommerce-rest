from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.product.urls')),
    path('api/v1/', include('rest_framework.urls')),
]
# TODO: add support 4 media