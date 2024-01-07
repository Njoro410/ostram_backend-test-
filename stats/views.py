from rest_framework.decorators import api_view
from savings.models import SavingsAccount, ReceiveSavings, WithdrawSavings
from deposits.models import DepositsAccount
from loans.models import Loans
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime, date, timedelta
from rest_framework import status
from django.db.models import Avg
from django.db import models
# Create your views here.


@api_view(['GET'])
def get_statistics(request):
    # Get current month and year
    today = date.today()
    current_month = today.month
    current_year = today.year

    # Calculate total savings this month
    total_savings = SavingsAccount.objects.filter(
        created_on__month=current_month, created_on__year=current_year).aggregate(total=Sum('savings_balance'))['total'] or 0

    # Calculate total loans given this month
    total_loans = Loans.objects.filter(created_on__month=current_month, created_on__year=current_year).aggregate(
        total=Sum('principal_amount'))['total'] or 0

    # Calculate total deposits this month
    total_deposits = DepositsAccount.objects.filter(
        created_on__month=current_month, created_on__year=current_year).aggregate(total=Sum('deposits_balance'))['total'] or 0
    total_loans_current_month = Loans.objects.filter(
        start_date__year=current_year).count()
    total_loans_current_year = Loans.objects.filter(
        start_date__year=current_year, start_date__month=current_month).count()
    total_received_savings_current_year = ReceiveSavings.objects.filter(
        received_date__year=current_year).aggregate(total=Sum('received_amount'))['total']
    total_withdrawn_savings_current_year = WithdrawSavings.objects.filter(
        received_date__year=current_year).aggregate(total=Sum('received_amount'))['total']

    end_date = date.today()
    start_date = end_date - timedelta(days=180)  # 6 months

    total_savings_start = SavingsAccount.objects.filter(
        created_on__gte=start_date, created_on__lt=end_date).aggregate(total=Sum('savings_balance'))['total']
    total_savings_end = SavingsAccount.objects.filter(
        created_on__lt=end_date).aggregate(total=Sum('savings_balance'))['total']
    # savings growth rate last six months
    savings_growth_rate = (
        (total_savings_end - total_savings_start) / total_savings_start) * 100

    start_date_avg_savings = date(current_year, 1, 1)
    end_date_avg_savings = date(current_year, 12, 31)

    total_received_savings = ReceiveSavings.objects.filter(
        received_date__range=(start_date_avg_savings, end_date_avg_savings)
    ).aggregate(total=Avg('received_amount'))['total']
    num_of_months = (end_date_avg_savings.year - start_date_avg_savings.year) * \
        12 + end_date_avg_savings.month - start_date_avg_savings.month + 1

    average_monthly_savings = total_received_savings / num_of_months

    # Query the savings_balance for each month until the current month
    savings_balance_array = SavingsAccount.objects.annotate(
        year=models.functions.ExtractYear('created_on'),
        month=models.functions.ExtractMonth('created_on')
    ).filter(
        year=current_year,
        month__lte=current_month
    ).values(
        'year', 'month'
    ).annotate(
        total_savings=Sum('savings_balance')
    ).order_by('year', 'month').values_list('total_savings', flat=True)

    # Convert the QuerySet to a list
    savings_balance_array = list(savings_balance_array)

    statistics = {
        'total_savings_current_month': total_savings,
        'total_loan_amount_current_month': total_loans,
        'total_deposits_current_month': total_deposits,
        'total_loans_current_month': total_loans_current_month,
        'savings_growth_rate_last_six_months': savings_growth_rate,
        'average_monthly_savings': average_monthly_savings,
        'total_savings_per_month': savings_balance_array
    }

    return Response(statistics, status=status.HTTP_200_OK)
