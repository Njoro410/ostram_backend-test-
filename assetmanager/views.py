from .models import loanAsset
from .serializers import AssetSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from loans.models import Loans
# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def loan_asset_by_loan_id(request, id):
    try:
        loan = get_object_or_404(Loans, id=id)
        asset = loanAsset.objects.filter(loan=loan)
    except loanAsset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssetSerializer(asset, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(loan=loan)
            return Response({"message": "Loan asset added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Loan asset creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = AssetSerializer(asset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan asset updated successfully", "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Loan asset updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        asset.delete()
        return Response({"message": "Loan document deleted successfullly"}, status=status.HTTP_204_NO_CONTENT)
    
    
    
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def specific_loan_asset(request, id):
    try:
        asset = loanAsset.objects.filter(id=id)
    except loanAsset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssetSerializer(asset, many=False)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = AssetSerializer(asset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan asset updated successfully", "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Loan asset updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        asset.delete()
        return Response({"message": "Loan document deleted successfullly"}, status=status.HTTP_204_NO_CONTENT)
