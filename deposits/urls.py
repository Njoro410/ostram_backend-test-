from django.urls import path
from . import views

urlpatterns = [
    path('total_deposits/',views.get_total_deposits,name='total_deposits'),
    path('member_deposits/<int:member_no>/',views.get_member_deposits,name='member_deposits'),
]
