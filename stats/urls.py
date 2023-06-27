from django.urls import path
from . import views

urlpatterns = [
    path('statistics/',views.get_statistics,name='get_statistics'),
]