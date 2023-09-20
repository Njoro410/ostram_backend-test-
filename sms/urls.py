from django.urls import path
from .views import send_single_sms,send_multiple_sms,broadcast_sms

urlpatterns = [
    path('send_single_sms/', send_single_sms, name='send_single_sms'),
    path('send_multiple_sms/', send_multiple_sms, name='send_bulk_sms'),
    path('broadcast/', broadcast_sms, name='broadcast_sms'),
]
