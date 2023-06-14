from django.urls import path

from . import views

urlpatterns = [
    # all stores near me
    path('', views.nearby_stores, name='nearby-stores'),
    # add product to store inventory
    path('inventory', views.store_inventory, name='new-store-product'),
    # get single product from a store
    path('inventory/<id>', views.store_inventory_products, name='store-product'),
    # get a single store
    path('<id>', views.store, name='single-store'),
]
