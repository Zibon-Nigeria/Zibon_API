from django.urls import path
from . import views

urlpatterns = [
    # all stores near me
    path('', views.stores, name='stores'),
    # new store
    path('new/', views.new_store, name='new-store'),
    # get single product from a store
    path('inventory/<id>/', views.store_product, name='store-product'),
    # my store
    path('my-store/', views.my_store, name='my store'),
    
    path('my-store/categories/', views.my_store_category, name='add new category'),
    path('my-store/categories/<id>', views.my_category, name='single category'),

    path('my-store/inventory/', views.my_store_inventory, name='add new-product'),
    path('my-store/inventory/<id>/', views.my_store_product, name='store-product'),
   
    path('my-store/orders/', views.all_order_items, name='all orders'),
    path('my-store/order-item/<id>/', views.single_order_item, name='single order'),
   
    path('<id>/', views.store, name='single-store'),
]
