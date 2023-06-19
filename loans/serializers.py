from .models import Loans, LoanProduct, Documents, DocumentType, LoanStatus
from rest_framework import serializers
# from members.serializers import MemberSerializer
from members.models import Members
from django.utils import timezone


class LoanDocumentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'description']


class LoanTypeSerializer(serializers.ModelSerializer):
    documents = LoanDocumentTypeSerializer(many=True, read_only=True)

    class Meta:
        model = LoanProduct
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = ['names', 'mbr_no', 'id_no']


class LoanSerializer(serializers.ModelSerializer):
    guarantors = MemberSerializer(many=True)
    lendee = serializers.SerializerMethodField()
    loan_product = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    is_grace_period = serializers.SerializerMethodField()
    remaining_grace_period = serializers.SerializerMethodField()

    def get_lendee(self, loan):
        lendee = loan.member.names
        return lendee

    def get_loan_product(self, loan):
        _type = loan.loan_product
        return _type.name

    def get_status(self, loan):
        status = loan.status
        return status.status_name
    
    def get_remaining_grace_period(self, loan):
        remaining_days = (loan.start_date + timezone.timedelta(days=loan.grace_period) - timezone.now().date()).days
        return remaining_days if remaining_days > 0 else 0
    
    def get_is_grace_period(self, loan):
        remaining_days = (loan.start_date + timezone.timedelta(days=loan.grace_period) - timezone.now().date()).days
        return 0 < remaining_days <= loan.grace_period

    

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
    
    def get_loan_owner(self,document_loan):
        lendee = document_loan.loan.member.names
        return lendee
    
    def get_status(self,document):
        status = document.status.status_name
        return status
    
    def get_created_by(self,document_creator):
        name = document_creator.created_by.fullname
        return name

    class Meta:
        model = Documents
        fields = "__all__"


class LoanStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanStatus
        fields = "__all__"
