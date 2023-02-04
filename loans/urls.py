from django.urls import path
from . import views

urlpatterns = [
    path('loantypes/',views.loan_types_create_add, name='loantypes'),
    path('loantypes/details/<int:id>/',views.loantype_detail, name='loantype_details'),
    path('all_loans/',views.get_all_loans, name='loans'),
    path('member_loans/<int:member_id>/',views.get_loans_by_member_id, name='loans_by_member_id'),
]
