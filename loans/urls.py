from django.urls import path
from . import views

urlpatterns = [
    path('loan_types/',views.loan_types_get_add, name='loantypes'),
    path('loantypes/details/<int:id>/',views.loantype_detail, name='loantype_details'),
    path('all_loans/',views.get_all_loans, name='loans'),
    path('member_loans/<int:member_no>/',views.get_loans_by_member_no, name='loans_by_member_no'),
    path('loan_documents/<int:loan_id>/',views.loan_documents_by_loan_id, name='loan_documents'),
    path('loan_status/', views.loan_status, name='loan_status')
]
