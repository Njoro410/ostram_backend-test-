from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DepositsSerializer
from rest_framework import status
from .models import DepositsAccount
from members.models import Members
from django.db.models import Sum
# Create your views here.


@api_view(['GET'])
def get_total_deposits(request):
    total_deposits = DepositsAccount.objects.all().aggregate(Sum('balance'))[
        'balance__sum']
    return Response({'total_deposits': total_deposits}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
# get deposits based on member number
def get_member_deposits(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        deposits = DepositsAccount.objects.filter(account_owner=member)
    except DepositsAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DepositsSerializer(deposits, many=True)
        return Response({"message":"Success", "data": serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = DepositsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Deposit Account created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Deposit Account creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        serializer = DepositsSerializer(deposits, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Deposit Account updated successfully", "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Deposit Account updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        deposits.delete()
        return Response({"message": "Deposit Account deleted successfullly"}, status=status.HTTP_204_NO_CONTENT)
