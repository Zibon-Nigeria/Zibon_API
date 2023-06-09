from django.urls import path

from . import views

urlpatterns = [
    # all stores near me
    path('', views.get_all_stores, name='stores'),
    # get a single store
    path('<id>', views.get_store, name='single-store'),
    # get single product from a store
    path('item/<id>', views.get_store_product, name='store-product'),
]
