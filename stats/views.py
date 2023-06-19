from rest_framework.decorators import api_view
from savings.models import SavingsAccount
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime
from rest_framework import status
# Create your views here.


@api_view(['GET'])
def get_total_savings_currentYear(request):
    try:
        current_year = datetime.now().year
        total_savings = SavingsAccount.objects.filter(
        created_on__year=current_year).aggregate(sum=Sum('savings_balance'))['sum']
    except SavingsAccount.DoesNotExist:
        return Response({'Error': 'There are no members'}, status=status.HTTP_404_NOT_FOUND)

    if total_savings is None:
        total_savings = 0.0

    return Response({f'total_savings_{current_year}': total_savings}, status=status.HTTP_200_OK)
