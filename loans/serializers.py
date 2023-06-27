from .models import Loans, LoanProduct, Documents, DocumentType, LoanStatus, Installment, DocumentStatus, LoanRepayment
from rest_framework import serializers
# from members.serializers import MemberSerializer
from members.models import Members
from django.utils import timezone


class LoanDocumentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'description']
        
class LoanDocumentStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentStatus
        fields = "__all__"


class LoanTypeSerializer(serializers.ModelSerializer):
    documents = LoanDocumentTypeSerializer(many=True, read_only=True)

    class Meta:
        model = LoanProduct
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['mbr_no']


class LoanSerializer(serializers.ModelSerializer):
    guarantors = serializers.PrimaryKeyRelatedField(many=True, queryset=Members.objects.all(), required=False)
    lendee = serializers.SerializerMethodField()
    loan_product_name = serializers.SerializerMethodField(read_only=True)
    status_name = serializers.SerializerMethodField(read_only=True)
    is_grace_period = serializers.SerializerMethodField(read_only=True)
    remaining_grace_period = serializers.SerializerMethodField(read_only=True)
    interest_type = serializers.SerializerMethodField(read_only=True)


    def get_lendee(self, loan):
        member = loan.member.names
        return member

    def get_loan_product_name(self, loan):
        _type = loan.loan_product
        return _type.name

    def get_status_name(self, loan):
        status = loan.status
        return status.status_name

    def get_remaining_grace_period(self, loan):
        remaining_days = (
            loan.start_date + timezone.timedelta(days=loan.grace_period) - timezone.now().date()).days
        return remaining_days if remaining_days > 0 else 0

    def get_is_grace_period(self, loan):
        remaining_days = (
            loan.start_date + timezone.timedelta(days=loan.grace_period) - timezone.now().date()).days
        return 0 < remaining_days <= loan.grace_period

    def get_interest_type(self, loan):
        _type = loan.loan_product.interest_type
        return _type


    class Meta:
        model = Loans
        fields = "__all__"


class LoanDocumentSerializer(serializers.ModelSerializer):
    document_type = serializers.SerializerMethodField()
    loan_owner = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    def get_document_type(self, document):
        _type = document.document_type
        return _type.name

    def get_loan_owner(self, document_loan):
        lendee = document_loan.loan.member.names
        return lendee

    def get_status(self, document):
        status = document.status.status_name
        return status

    def get_created_by(self, document_creator):
        name = document_creator.created_by.fullname
        return name

    class Meta:
        model = Documents
        fields = "__all__"


class LoanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanStatus
        fields = "__all__"
        
class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = "__all__"


class LoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = "__all__"