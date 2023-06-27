from django.urls import path
from . import views

urlpatterns = [
    path('total_savings/',views.get_total_savings,name='total_savings'),
    path('member_savings/<int:member_no>/',views.get_member_savings,name='member_savings'),
    path('add_savings/<int:member_no>/',views.add_savings,name='add_member_savings'),
]
