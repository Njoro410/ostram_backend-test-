from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import DailyContributionsSerializer
from rest_framework import status
from .models import DailyContributions
from rest_framework.permissions import IsAuthenticated
from deposits.models import ReceiveDeposits
from loans.models import LoanRepayment,Loans
from loans.views import get_disbursed_loan_by_member
from loans.serializers import LoanRepaymentSerializer
from savings.models import ReceiveSavings,SavingsAccount
from deposits.models import ReceiveDeposits,DepositsAccount
from decimal import Decimal


# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def daily_contributions(request):
    try:
        all_contributions = DailyContributions.objects.all()

    except DailyContributions.DoesNotExist:
        return Response(
            {"error": "There are no daily contributions"},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = DailyContributionsSerializer(all_contributions, many=True)
    return Response(
        {"message": "Success", "results": serializer.data},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def add_contributions(request):
    serializer = DailyContributionsSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        member = data.get('member')


        # Check if the member has an active loan
        active_loan = Loans.objects.filter(member=member, is_active=True).first()

        if active_loan:
            # Member has an active loan, create a loan repayment record
            loan_repayment_data = {
                'loan': active_loan.pk,
                'payment_amount': data.get('loan_repayment', Decimal('0.00')),
                'payment_date': data.get('collection_date'),
                'created_by': request.user.pk,
                'updated_by': request.user.pk,
            }

            loan_repayment_serializer = LoanRepaymentSerializer(data=loan_repayment_data)
            if loan_repayment_serializer.is_valid():
                loan_repayment_serializer.save()

            else:
                return Response(
                    {"message": "Loan repayment failed", "errors": loan_repayment_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Process savings and deposits contributions 
        savings_account = SavingsAccount.objects.get(account_owner=member)
        savings_data = {
            'account': savings_account,
            'received_amount': data.get('savings', Decimal('0.00')),
            'received_date': data.get('collection_date'),
            'created_by': request.user,
            'updated_by': request.user,
        }

        receive_savings_instance = ReceiveSavings.objects.create(**savings_data)

        deposits_account = DepositsAccount.objects.get(account_owner=member)
        deposits_data = {
            'account': deposits_account,
            'received_amount': data.get('deposits', Decimal('0.00')),
            'received_date': data.get('collection_date'),
            'created_by': request.user,
            'updated_by': request.user,
        }

        receive_deposits_instance = ReceiveDeposits.objects.create(**deposits_data)
        serializer.save()
        return Response(
            {"message": "Success", "results": serializer.data},
            status=status.HTTP_201_CREATED,
        )
        
    else:
        return Response(
            {"message": "Contribution posting failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def member_contributions(request, mbr_no):
    try:
        contributions = DailyContributions.objects.filter(account_no=mbr_no)

    except DailyContributions.DoesNotExist:
        return Response(
            {"error": "This member does not have contributions"},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = DailyContributionsSerializer(contributions, many=True)
    return Response(
        {"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK
    )
