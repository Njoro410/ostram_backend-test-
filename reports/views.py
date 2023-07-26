from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from savings.models import ReceiveSavings
from loans.models import LoanRepayment
from deposits.models import ReceiveDeposits
# from administration.models import globalCharges
from loans.serializers import LoanRepaymentSerializer
from savings.serializers import AddSavingsSerializer
from deposits.serializers import AddDepositsSerializer

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_filtered_transactions(request):
    transactions = []
    year = request.query_params.get('year')
    month = request.query_params.get('month')

        # Validate the year parameter if provided
    try:
        if year is not None:
            year = int(year)
    except ValueError:
        return Response({'error': 'Invalid year format. Year must be a valid integer.'}, status=status.HTTP_400_BAD_REQUEST)

    # Validate the month parameter if provided
    try:
        if month is not None:
            month = int(month)
            if not 1 <= month <= 12:
                raise ValueError
    except ValueError:
        return Response({'error': 'Invalid month format. Month must be a valid integer between 1 and 12.'}, status=status.HTTP_400_BAD_REQUEST)
    
    models_to_serialize = {
        LoanRepayment: LoanRepaymentSerializer,
        ReceiveSavings: AddSavingsSerializer,
        ReceiveDeposits: AddDepositsSerializer,
        # Add other models and serializers here if needed
    }

    # create a queryset to be used for all models
    if year and month:
        # Filter transactions for a specific month of a specific year
        queryset = Q(created_on__year=year, created_on__month=month)
    elif year:
        # Filter transactions for the entire year
        queryset = Q(created_on__year=year)
    else:
        # No year or month provided, return all transactions
        queryset = Q()

    for model, serializer_class in models_to_serialize.items():
        model_name = model.__name__
        items = model.objects.filter(queryset)

        if items.exists():
            data = serializer_class(items, many=True).data
            transactions.append({model_name: data})
        else:
            '''
            appends empty array if transactions don't exist
            '''
            transactions.append({model_name: []})

    return Response({"message":"Success", "response": transactions}, status=status.HTTP_200_OK)

