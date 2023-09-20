from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import DailyContributionsSerializer
from rest_framework import status
from .models import DailyContributions
from rest_framework.permissions import IsAuthenticated
from deposits.models import ReceiveDeposits
from loans.models import LoanRepayment
from savings.models import ReceiveSavings
from loans.views import get_disbursed_loan_by_member


# Create your views here.
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def daily_contributions(request):
    if request.method == "GET":
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

    elif request.method == "POST":
        serializer = DailyContributionsSerializer(data=request.data)
        if serializer.is_valid():
            # Extract contribution data from serializer
            data = serializer.validated_data
            deposit_amount = data.get("deposits", 0)
            loan_amount = data.get("loan_repayment", 0)
            loan_interest = data.get("loan_interest", 0)
            savings_amount = data.get("savings", 0)
            account = data.get("account_no")

            # Create instances for deposit, loan, and savings
            if deposit_amount > 0:
                receive_deposit = ReceiveDeposits(
                    account=account,
                    received_amount=deposit_amount,
                    received_date=data["received_date"],
                    created_by=request.user,
                )
                receive_deposit.save()

            if loan_amount > 0:
                disbursed_loan = get_disbursed_loan_by_member(account)
                receive_loan = LoanRepayment(
                    payment_amount=loan_amount + loan_interest,
                    payment_date=data["received_date"],
                    created_by=request.user,
                    loan=disbursed_loan,
                )
                receive_loan.save()

            if savings_amount > 0:
                receive_savings = ReceiveSavings(
                    account=account,
                    received_amount=savings_amount,
                    received_date=data["received_date"],
                    created_by=request.user,
                )
                receive_savings.save()

            # Continue with creating the contribution instance
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
