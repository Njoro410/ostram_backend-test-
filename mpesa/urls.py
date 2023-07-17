from django.urls import path
from .views import get_access_token, make_mpesa_express_request, mpesa_callback, transaction_status, transaction_status_callback, c2b_confirmation_register, c2b_confirmation_callback, c2b_confirmation_validation


urlpatterns = [
    path('access_token/', get_access_token, name="get_access_token"),
    path('stk-push/', make_mpesa_express_request,
         name="send_Stk_push_to_number"),
    path('mpesa_callback/', mpesa_callback, name="lipa_na_mpesa_callback"),
    path('transaction_status/', transaction_status, name="transaction_status"),
    path('transaction_status_callback/',
         transaction_status_callback, name="transaction_status"),
    path('c2b_confirmation_register/', c2b_confirmation_register,
         name="c2b_confirmation_register"),
    path('c2b_confirmation_callback/', c2b_confirmation_callback,
         name="c2b_confirmation_callback"),
    path('c2b_confirmation_validation/', c2b_confirmation_validation,
         name="c2b_confirmation_validation"),
]
