from django.urls import path
from . import views

urlpatterns = [
    path('total_savings/',views.get_total_savings,name='total_savings'),
    path('saving_accounts/',views.get_saving_accounts, name='saving accounts'),
    path('member_savings/<int:member_no>/',views.get_member_savings,name='member_savings'),
    path('add_savings/<int:member_no>/',views.add_savings,name='add_member_savings'),
    path('withdraw_savings/<int:member_no>/',views.withdraw_savings,name='add_member_savings'),
    path('members/<str:member_no>/savings_received/', views.get_savings_received),
    path('members/<str:member_no>/savings_withdrawals/', views.get_withdrawals)
]
