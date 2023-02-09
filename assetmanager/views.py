from .models import loanAsset
from .serializers import AssetSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from loans.models import Loans
# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def loan_asset_by_loan_id(request,id):
    try:
        asset = loanAsset.objects.filter(loan_id=id)
    except loanAsset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AssetSerializer(asset, many=True)

        return Response({"message":"Success", "results": serializer.data}, status=status.HTTP_200_OK)
    
    
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def loan_asset_document(request,id):
#     try:
#         asset_document = assetDocument.objects.filter(proof_of=id)
#     except assetDocument.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = AssetDocumentSerializer(asset_document, many=True)

#         return Response({"message":"Success", "results": serializer.data}, status=status.HTTP_200_OK)