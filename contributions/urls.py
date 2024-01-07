from django.urls import path
from . import views

urlpatterns = [
    path('daily_contributions/',views.daily_contributions,name='daily_contributions'),
    path('add_contributions/',views.add_contributions,name='add contributions'),
    path('member_contributions/<int:mbr_no>/',views.member_contributions,name='member_contributions'),
]
