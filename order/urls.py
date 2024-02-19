from django.urls import path
from . import views

urlpatterns = [
    path('', views.make_order, name='make_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('<str:order_number>/', views.single_order, name='get_order'),
    path('<str:order_number>/update/', views.update_order, name='update_order'),
    path('<str:order_number>/paid/', views.set_paid, name='set_paid'),
    path('deliveries/<id>/', views.single_delivery, name='single_delivery'),
    path('deliveries/<id>/accept/', views.accept_delivery, name='accept_delivery'),
]
