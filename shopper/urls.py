from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('bank-info/', views.bank_info, name="bank-info"),
    path('bank-info/<id>', views.bank, name="bank-details"),
    path('personal-info/', views.shopper_personal_info, name="personal-info"),
    path('deliveries/', views.available_deliveries, name="available-deliveries"),
    path('deliveries/history/', views.delivery_history, name="delivery-history"),
    path('deliveries/history/<id>', views.delivery_history_detail, name="history-details"),
    path('deliveries/<id>/', views.delivery, name="delivery-detail"),
]
