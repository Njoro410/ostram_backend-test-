from django.urls import path
from .import views


urlpatterns = [
    path('loan_assets/<int:id>/',views.loan_asset_by_loan_id,name='loan_assets'),
    path('loan_assets/',views.loan_asset_by_loan_id,name='loan_assets_without_id'),
    path('loan_asset_document/<int:loan_asset_id>/',views.loan_asset_documents,name='loan_asset_document'),
    path('loan_asset_document/',views.loan_asset_documents,name='loan_asset_document_without_id'),
]
