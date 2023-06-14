from .models import Loans, Loan_Type, Documents, documentType, Loan_Status
from rest_framework import serializers
# from members.serializers import MemberSerializer
from members.models import members


class LoanDocumentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = documentType
        fields = ['id', 'name', 'description']


class LoanTypeSerializer(serializers.ModelSerializer):
    documents = LoanDocumentTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Loan_Type
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = members
        fields = ['names', 'mbr_no', 'id_no']


class LoanSerializer(serializers.ModelSerializer):
    guarantors = MemberSerializer(many=True)
    lendee = serializers.SerializerMethodField()
    loan_type = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_lendee(self, loan):
        lendee = loan.lendee
        return lendee.names

    def get_loan_type(self, loan):
        _type = loan.loan_type
        return _type.name

    def get_status(self, loan):
        status = loan.status
        return status.status_name

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
        lendee = document_loan.loan.lendee.names
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
        model = Loan_Status
        fields = "__all__"
