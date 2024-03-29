from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/my-orders', views.my_orders, name='my-orders'),
    path('profile/delete-account', views.delete_account, name='delete account'),
]