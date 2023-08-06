from django.urls import path

from . import views

urlpatterns = [
    path('order/', views.make_order, name='make_order'),
    path('order/request-delivery', views.request_delivery, name='request-delivery'),
    # path('profile/', views.my_profile, name='my-profile'),
]
