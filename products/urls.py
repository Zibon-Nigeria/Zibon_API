from django.urls import path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Products API')

from . import views

urlpatterns = [
    path('', views.products, name='all-products'),
    path('categories', views.categories, name='categories'),
    path('categories/<slug:slug>', views.get_category, name='single-category'),
    path('<id>', views.get_product, name='single-products'),
]
