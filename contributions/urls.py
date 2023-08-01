from django.urls import path
from . import views

urlpatterns = [
    path('daily_contributions/',views.daily_contributions,name='daily_contributions'),
]
