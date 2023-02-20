from django.urls import path
from .import views


urlpatterns = [
    path('loan_assets/<int:id>/',views.loan_asset_by_loan_id,name='loan_assets'),
    path('loan_asset_document/<int:id>/',views.specific_loan_asset,name='loan_asset_document'),
]
