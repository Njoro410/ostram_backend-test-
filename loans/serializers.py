from .models import Loans, Loan_Type, Documents, documentType
from rest_framework import serializers

class LoanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan_Type
        fields = "__all__"