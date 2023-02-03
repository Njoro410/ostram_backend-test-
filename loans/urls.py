from django.urls import path
from . import views

urlpatterns = [
    path('loantypes/',views.loantypes, name='loantypes'),
]
