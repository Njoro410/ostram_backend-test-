from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SavingsSerializer, AddSavingsSerializer
from rest_framework import status
from .models import SavingsAccount, ReceiveSavings
from members.models import Members
from django.db.models import Sum
# Create your views here.


@api_view(['GET'])
def get_total_savings(request):
    total_savings = SavingsAccount.objects.all().aggregate(Sum('savings_balance'))[
        'savings_balance__sum']
    return Response({'total_savings': total_savings}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
# get savings based on member number
def get_member_savings(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        savings = SavingsAccount.objects.filter(account_owner=member)
    except SavingsAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SavingsSerializer(savings, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    # elif request.method == 'POST':
    #     serializer = SavingsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Savings Account created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    #     return Response({"message": "Savings Account creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'PUT':
    #     serializer = SavingsSerializer(savings, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Savings Account updated successfully", "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
    #     return Response({"message": "Savings Account updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        savings.delete()
        return Response({"message": "Savings Account deleted successfullly"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
# get savings based on member number
def add_savings(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        print(member.mbr_no)
        account = get_object_or_404(SavingsAccount, account_owner=member.mbr_no)
        print(account)
    except SavingsAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AddSavingsSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(account=account)
        return Response({"message": "Amount added", "results": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
