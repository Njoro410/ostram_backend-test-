from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DepositsSerializer, AddDepositsSerializer, WithdrawalsSerializer, WithdrawDepositsSerializer, DepositsReceivedSerializer
from rest_framework import status
from .models import DepositsAccount, ReceiveDeposits, WithdrawDeposits
from members.models import Members
from django.db.models import Sum, Count
# Create your views here.


@api_view(['GET'])
def get_total_deposits(request):
    total_deposits = DepositsAccount.objects.all().aggregate(Sum('balance'))[
        'balance__sum']
    return Response({'total_deposits': total_deposits}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_deposit_accounts(request):
    try:
        all_accounts = DepositsAccount.objects.all()
    except DepositsAccount.DoesNotExist:
        return Response(
            {"Error": "No accounts found"}, status=status.HTTP_404_NOT_FOUND
        )
    serializer = DepositsSerializer(all_accounts, many=True)

    return Response(
        {"message": "Success", "results": serializer.data},
        status=status.HTTP_200_OK,
    )


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
        return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)

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


@api_view(['POST'])
# get savings based on member number
def add_deposits(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        account = get_object_or_404(
            DepositsAccount, account_owner=member.mbr_no)
    except DepositsAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AddDepositsSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(account=account)
        return Response({"message": "Amount added", "results": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# get savings based on member number
def withdraw_deposits(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        account = get_object_or_404(
            DepositsAccount, account_owner=member.mbr_no)
    except DepositsAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = WithdrawDepositsSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(account=account)
        return Response({"message": "Amount widthdrawn", "results": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_deposits_received(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        deposits_account = get_object_or_404(
            DepositsAccount, account_owner=member)
    except Members.DoesNotExist:
        return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
    except DepositsAccount.DoesNotExist:
        return Response({"message": "Deposits account not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve all savings received
    all_received_deposits = ReceiveDeposits.objects.filter(
        account=deposits_account)

    # Get total savings for each month
    monthly_deposits_totals = all_received_deposits.values('received_date__year', 'received_date__month') \
        .annotate(total_received=Sum('received_amount'), count=Count('received_amount'))

    serializer = DepositsReceivedSerializer({
        "all_received_deposits": all_received_deposits,
        "monthly_deposits_totals": monthly_deposits_totals
    })

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_deposit_withdrawals(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        deposits_account = get_object_or_404(
            DepositsAccount, account_owner=member)
    except Members.DoesNotExist:
        return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
    except DepositsAccount.DoesNotExist:
        return Response({"message": "Savings account not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve all withdrawals
    all_withdrawals = WithdrawDeposits.objects.filter(account=deposits_account)

    # Get total withdrawals for each month
    monthly_withdrawals_totals = all_withdrawals.values('withdrawn_date__year', 'withdrawn_date__month') \
        .annotate(total_withdrawn=Sum('withdrawn_amount'), count=Count('withdrawn_amount'))

    serializer = WithdrawalsSerializer({
        "all_withdrawals": all_withdrawals,
        "monthly_withdrawals_totals": monthly_withdrawals_totals
    })

    return Response(serializer.data, status=status.HTTP_200_OK)
