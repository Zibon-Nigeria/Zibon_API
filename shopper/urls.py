from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard),
    path('bank-info/', views.bank_info),
    path('bank-info/<id>', views.bank),
    path('personal-info/', views.shopper_personal_info),
    path('deliveries/<id>/', views.delivery),
]
