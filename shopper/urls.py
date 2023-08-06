from django.urls import path
from . import views

urlpatterns = [
    path('shopper/dashboard/', views.dashboard, name="dashboard"),
    path('shopper/bank-info/', views.bank_info, name="bank-info"),
    path('shopper/bank-info/<id>', views.bank, name="bank-details"),
    path('shopper/personal-info/', views.shopper_personal_info, name="personal-info"),
    path('shopper/deliveries/', views.available_deliveries, name="available-deliveries"),
    path('shopper/deliveries/history/', views.delivery_history, name="delivery-history"),
    path('shopper/deliveries/history/<id>', views.delivery_history_detail, name="history-details"),
    path('shopper/deliveries/<id>/', views.delivery, name="delivery-detail"),
]
