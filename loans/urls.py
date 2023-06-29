from django.urls import path
from . import views

urlpatterns = [
    path('loan_types/',views.loan_types_get_add, name='loantypes'),
    path('loantypes/details/<int:id>/',views.loantype_detail, name='loantype_details'),
    path('all_loans/',views.get_loans_by_member_no, name='loans without an id'),
    path('member_loans/<int:member_no>/',views.get_loans_by_member_no, name='loans_by_member_no'),
    path('loan_documents/<int:loan_id>/',views.loan_documents_by_loan_id, name='loan_documents'),
    path('loan_status/', views.loan_status, name='loan_status'),
    path('loan_document_status/', views.document_status, name='document_status'),
    path('loan_document_types/<int:id>/', views.documentTypes, name='loan_document_types'),
    path('loan_document_types/', views.documentTypes, name='loan_document_types_no_id'),
    path('loan_documents/',views.loan_documents_by_loan_id, name='loan_documents_no_id'),
    path('create_loan/',views.create_loan, name='create_new_loan'),
    path('loan/<int:loan_id>/',views.get_loans_by_loan_id, name='get_loans_by_loan_id'),
    path('installments/<int:loan_id>/',views.get_installments_by_loan_id, name='get_installments_by_loan_id'),
    path('pay_loan/',views.pay_loan, name='pay_loan'),
    path('update_loan/<int:loan_id>/',views.update_loan, name='update_loan'),
]
