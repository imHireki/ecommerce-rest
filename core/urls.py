from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('api/v1/', include('apps.product.urls')),
    path('api/v1/', include('rest_framework.urls')),
]

# Serving MEDIA
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
