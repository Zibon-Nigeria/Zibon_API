from django.urls import path

from . import views

urlpatterns = [
    path('', views.make_order, name='make_order'),
    path('<id>/', views.make_order, name='get_order'),
    path('<id>/update/', views.make_order, name='update_order'),
    path('deliveries/', views.request_delivery, name='request_delivery'),
    path('deliveries/<id>/accept/', views.request_delivery, name='accept_delivery'),
    path('deliveries/<id>/update/', views.request_delivery, name='update_delivery'),
]
