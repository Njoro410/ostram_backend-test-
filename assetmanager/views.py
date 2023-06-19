from .models import loanAsset, assetDocument
from .serializers import AssetSerializer, AssetDocumentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from loans.models import Loans
# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def loan_asset_by_loan_id(request, id=None):
    if request.method == 'GET':
        if id is None:
            all_assets = loanAsset.objects.all()
            serializer = AssetSerializer(all_assets, many=True)
            return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                loan = get_object_or_404(Loans, id=id)
                asset = loanAsset.objects.filter(loan=loan)
            except loanAsset.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        
        serializer = AssetSerializer(asset, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

        if request.method == 'POST':
            serializer = AssetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(loan=loan)
                return Response({"message": "Loan asset added successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"message": "Loan asset creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            serializer = AssetSerializer(asset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Loan asset updated successfully", "results": serializer.data}, status=status.HTTP_202_ACCEPTED)
            return Response({"message": "Loan asset updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            asset.delete()
            return Response({"message": "Loan document deleted successfullly"}, status=status.HTTP_204_NO_CONTENT)





@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def loan_asset_documents(request, loan_asset_id=None):
    if request.method == 'GET':
        if loan_asset_id is None:
            all_asset_documents = assetDocument.objects.all()
            serializer = AssetDocumentSerializer(
                all_asset_documents, many=True)
            return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                loan_asset = get_object_or_404(loanAsset, id=loan_asset_id)
                asset_document = assetDocument.objects.filter(
                    proof_of=loan_asset)
            except assetDocument.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AssetDocumentSerializer(asset_document, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

        if request.method == 'POST':
            serializer = AssetDocumentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(proof_of=loan_asset)
                return Response({"message": "Loan asset document added successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"message": "Loan asset document creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            serializer = AssetDocumentSerializer(loan_asset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Loan asset document updated successfully", "results": serializer.data}, status=status.HTTP_202_ACCEPTED)
            return Response({"message": "Loan asset document updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            loan_asset.delete()
            return Response({"message": "Loan asset document deleted successfullly"}, status=status.HTTP_204_NO_CONTENT)
