from django.urls import path
from . import views

urlpatterns = [
    # all stores near me
    path('', views.stores, name='stores'),
    # new store
    path('new/', views.new_store, name='new-store'),
    # get a single store
    path('<id>/', views.store, name='single-store'),
    # get single product from a store
    path('inventory/<id>/', views.store_product, name='store-product'),
    # my store
    path('my-store/', views.my_store, name='my store'),
    # add product to store inventory
    path('my-store/inventory/', views.my_store_inventory, name='add new-product'),
    # get single product from a store
    path('my-store/inventory/<id>/', views.my_store_product, name='store-product'),
    # add product to store inventory
    path('my-store/orders/', views.all_order_items, name='all orders'),
    # get single product from a store
    path('my-store/order-item/<id>/', views.single_order_item, name='single order'),
]
