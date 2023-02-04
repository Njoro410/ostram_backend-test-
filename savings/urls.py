from django.urls import path
from . import views

urlpatterns = [
    path('total_savings/',views.get_total_savings,name='total_savings')
]
