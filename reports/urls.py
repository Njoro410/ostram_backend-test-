from django.urls import path
from .views import get_filtered_transactions

urlpatterns = [
     path('transactions/', get_filtered_transactions, name='transactions/report'),
]
