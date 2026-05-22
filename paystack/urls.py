from django.urls import path
from .views import initialize_payment, verify_payment

urlpatterns = [
    path('initialize/', initialize_payment, name='paystack-initialize'),
    path('verify/<str:reference>/', verify_payment, name='paystack-verify'),
]