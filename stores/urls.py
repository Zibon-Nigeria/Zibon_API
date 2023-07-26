from django.urls import path

from . import views

urlpatterns = [
    # all stores near me
    path('', views.stores, name='nearby-stores'),
    # new store
    path('new/', views.new_store, name='new store'),
    # my store
    path('my-store/', views.my_store, name='my store'),
    # add product to store inventory
    path('my-store/inventory', views.store_inventory, name='add new-product'),
    # get single product from a store
    path('inventory/<id>', views.store_product, name='store-product'),
    # get a single store
    path('<id>', views.store, name='single-store'),
]
