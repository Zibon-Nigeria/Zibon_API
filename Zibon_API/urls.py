"""
URL configuration for zibon_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt

from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Zibon API",
        default_version='v1',
        description="Zibon API",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="<EMAIL>"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # apps
    # path('api/products/', include('products.urls')),
    path('api/orders/', include('order.urls')),
    path('api/shopper/', include('shopper.urls')),
    path('api/stores/', include('stores.urls')),

    # authentication routes
    path('api/auth/', include('accounts.urls')),
    path('api/auth/login/', jwt.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/login/refresh/', jwt.TokenRefreshView.as_view(), name='token_refresh'),
    
    # path('docs/', include_docs_urls(title='Todo Api')),
    # urls(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# if settings.LOCAL_SERVE_MEDIA_FILES:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)