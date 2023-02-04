from django.urls import path
from . import views

urlpatterns = [
    path('loantypes/',views.loan_types_create_add, name='loantypes'),
    path('loantypes/details/<int:id>/',views.loantype_detail, name='loantype_details'),
]
