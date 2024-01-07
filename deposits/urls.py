from django.urls import path
from . import views

urlpatterns = [
    path('total_deposits/',views.get_total_deposits,name='total_deposits'),
    path('deposits_accounts/',views.get_deposit_accounts, name='saving accounts'),
    path('member_deposits/<int:member_no>/',views.get_member_deposits,name='member_deposits'),
    path('add_deposits/<int:member_no>/',views.add_deposits,name='add_member_deposits'),
    path('withdraw_deposits/<int:member_no>/',views.withdraw_deposits,name='withdraw_member_savings'),
    path('members/<str:member_no>/deposits_received/', views.get_deposits_received),
    path('members/<str:member_no>/deposits_withdrawals/', views.get_deposit_withdrawals)
]
 