from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SavingsSerializer, AddSavingsSerializer, WithdrawSavingsSerializer, SavingsReceivedSerializer, WithdrawalsSerializer
from rest_framework import status
from .models import SavingsAccount, ReceiveSavings, WithdrawSavings
from members.models import Members
from contributions.models import DailyContributions
# from django.db.models import Sum

from datetime import datetime
from django.db.models import Sum, Count

# Create your views here.


@api_view(['GET'])
def get_total_savings(request):
    total_savings = SavingsAccount.objects.all().aggregate(Sum('savings_balance'))[
        'savings_balance__sum']
    return Response({'total_savings': total_savings}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_saving_accounts(request):
    try:
        all_accounts = SavingsAccount.objects.all()
    except SavingsAccount.DoesNotExist:
        return Response(
            {"Error": "No accounts found"}, status=status.HTTP_404_NOT_FOUND
        )
    serializer = SavingsSerializer(all_accounts, many=True)

    return Response(
        {"message": "Success", "results": serializer.data},
        status=status.HTTP_200_OK,
    )


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

    elif request.method == 'DELETE':
        savings.delete()
        return Response({"message": "Savings Account deleted successfullly"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
# get savings based on member number
def add_savings(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        account = get_object_or_404(
            SavingsAccount, account_owner=member.mbr_no)
    except SavingsAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = AddSavingsSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(account=account)

        # Update DailyContributions model
        daily_contributions, created = DailyContributions.objects.get_or_create(
            member=member,
            collection_date=request.data.get('received_date'),
            total_amount=request.data.get('received_amount'),
            savings=request.data.get('received_amount')
        )
        daily_contributions.save()

        return Response({"message": "Amount added", "results": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# get savings based on member number
def withdraw_savings(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        print(member.mbr_no)
        account = get_object_or_404(
            SavingsAccount, account_owner=member.mbr_no)
        print(account)
    except SavingsAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = WithdrawSavingsSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(account=account)
        return Response({"message": "Amount widthdrawn", "results": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_savings_received(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        savings_account = get_object_or_404(
            SavingsAccount, account_owner=member)
    except Members.DoesNotExist:
        return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
    except SavingsAccount.DoesNotExist:
        return Response({"message": "Savings account not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve all savings received
    all_received_savings = ReceiveSavings.objects.filter(
        account=savings_account)

    # Get total savings for each month
    monthly_savings_totals = all_received_savings.values('received_date__year', 'received_date__month') \
        .annotate(total_received=Sum('received_amount'), count=Count('received_amount'))

    serializer = SavingsReceivedSerializer({
        "all_received_savings": all_received_savings,
        "monthly_savings_totals": monthly_savings_totals
    })

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_withdrawals(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        savings_account = get_object_or_404(
            SavingsAccount, account_owner=member)
    except Members.DoesNotExist:
        return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
    except SavingsAccount.DoesNotExist:
        return Response({"message": "Savings account not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve all withdrawals
    all_withdrawals = WithdrawSavings.objects.filter(account=savings_account)

    # Get total withdrawals for each month
    monthly_withdrawals_totals = all_withdrawals.values('withdrawn_date__year', 'withdrawn_date__month') \
        .annotate(total_withdrawn=Sum('withdrawn_amount'), count=Count('withdrawn_amount'))

    serializer = WithdrawalsSerializer({
        "all_withdrawals": all_withdrawals,
        "monthly_withdrawals_totals": monthly_withdrawals_totals
    })

    return Response(serializer.data, status=status.HTTP_200_OK)
