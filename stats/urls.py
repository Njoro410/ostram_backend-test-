from django.urls import path
from . import views

urlpatterns = [
    path('total_savings_yearly/',views.get_total_savings_currentYear,name='total_savings_yearly'),
]