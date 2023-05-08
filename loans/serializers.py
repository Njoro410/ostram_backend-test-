from .models import Loans, Loan_Type, Documents, documentType
from rest_framework import serializers

class LoanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan_Type
        fields = "__all__"
        
        
class LoanSerializer(serializers.ModelSerializer):
    # borrower_membership_number = serializers.ReadOnlyField()
    # guarantors = MemberSerializer(many=True)
    class Meta:
        model = Loans
        fields = "__all__"
        
class LoanDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"