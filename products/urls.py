from django.urls import path

from . import views

urlpatterns = [
    # path('', views.product_search, name='products-search'),
    path('categories', views.get_categories, name='categories'),
    path('categories/<slug:slug>', views.get_category, name='single-category'),
    path('<id>', views.get_product, name='single-products'),
]
