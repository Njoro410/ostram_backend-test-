from django.shortcuts import render
from .models import Installment, LoanProduct, Documents, DocumentType, LoanStatus, Loans, DocumentStatus
from .serializers import LoanTypeSerializer, LoanSerializer, LoanDocumentSerializer, LoanStatusSerializer, LoanDocumentTypeSerializer, InstallmentSerializer, LoanDocumentStatusSerializer, LoanRepaymentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from members.models import Members
from django.shortcuts import get_object_or_404
from datetime import date
from sms.utils import send_loan_status_sms,send_guarantors_text
# Create your views here.


@api_view(['GET', 'POST'])
def loan_types_get_add(request):
    """
    function to list and add loan types
    """
    if request.method == 'GET':
        types = LoanProduct.objects.all()
        serializer = LoanTypeSerializer(types, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = LoanTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan type created successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Loan type creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def loantype_detail(request, id):
    """
    Retrieve, update or delete a loan type.
    """
    try:
        loantype = LoanProduct.objects.get(id=id)
    except LoanProduct.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LoanTypeSerializer(loantype)
        return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = LoanTypeSerializer(loantype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan type updated successfully", "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Loan type updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        loantype.delete()
        return Response({"message": "Loan type deleted successfullly"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
# a function got getting and creating loan status
def loan_status(request):
    if request.method == 'GET':
        try:
            loan_status = LoanStatus.objects.all()
        except LoanStatus.DoesNotExist():
            return Response({'Error': 'Loan status not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LoanStatusSerializer(loan_status, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = LoanStatusSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan status created successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Loan status creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_loan(request):
    serializer = LoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Loan created succesfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"message": "Failed", "results": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
# get loan by loan id
def get_loans_by_loan_id(request, loan_id):
    try:
        loan = Loans.objects.get(id=loan_id)
    except Loans.DoesNotExist:
        return Response({'message': 'Loan does not exist'}, status=status.HTTP_404_NOT_FOUND)
    serializer = LoanSerializer(loan)
    return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def update_loan(request, loan_id):
    try:
        loan = Loans.objects.get(id=loan_id)
    except Loans.DoesNotExist:
        return Response({'message': 'Loan does not exist'}, status=status.HTTP_404_NOT_FOUND)

    new_status_id = request.data.get('id')
    new_guarantors = request.data.get('guarantors')
    send_text = request.data.get('text')
    clear_guarantors = request.data.get('clear')


    if new_status_id:
        try:
            new_status = LoanStatus.objects.get(id=new_status_id)
            # Update the loan status field in the database
            Loans.objects.filter(id=loan_id).update(status=new_status)
            if send_text:
                send_loan_status_sms(loan_id,new_status.status_name)

            # Check if the new status is "disbursed"
            if new_status.status_name == "DISBURSED":
                new_start_date = date.today()
                Loans.objects.filter(id=loan_id).update(
                    start_date=new_start_date)
        except LoanStatus.DoesNotExist:
            return Response({'message': 'Invalid status ID'}, status=status.HTTP_400_BAD_REQUEST)

    if new_guarantors:
        if clear_guarantors:
            loan.guarantors.clear()  # Clear existing guarantors
        for guarantor_id in new_guarantors:
            try:
                guarantor = Members.objects.get(mbr_no=guarantor_id)
                loan.guarantors.add(guarantor)
                if send_text:
                    send_guarantors_text(loan_id,guarantor_id)
            except Members.DoesNotExist:
                return Response({'message': 'Invalid guarantor ID'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if clear_guarantors:
            loan.guarantors.clear()  # Clear existing guarantors

    serializer = LoanSerializer(loan)
    return Response({"message": "Loan updated successfully", "results": serializer.data},
                    status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# get loans based on member no
def get_loans_by_member_no(request, member_no=None):
    if request.method == 'GET':
        # if no member id, return all loans
        if member_no is None:
            loans = Loans.objects.all()
            if not loans:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = LoanSerializer(loans, many=True)
            return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                member = get_object_or_404(Members, mbr_no=member_no)
                loan = Loans.objects.filter(member=member)
            except Loans.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LoanSerializer(loan, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = LoanSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan updated successfully", "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Loan updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_installments_by_loan_id(request, loan_id):
    try:
        installments = Installment.objects.filter(loan=loan_id)
    except Installment.DoesNotExist:
        return Response({'message': 'No Installments'}, status=status.HTTP_404_NOT_FOUND)
    serializer = InstallmentSerializer(installments, many=True)
    return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def loan_documents_by_loan_id(request, loan_id=None):
    if request.method == 'GET':
        if loan_id is None:
            all_documents = Documents.objects.all()
            serializer = LoanDocumentSerializer(all_documents, many=True)
            return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                loan = get_object_or_404(Loans, id=loan_id)
                documents = Documents.objects.filter(loan=loan)
            except Loans.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LoanDocumentSerializer(documents, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = LoanDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan document created successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Loan document creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = LoanDocumentSerializer(documents, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan document updated successfully", "results": serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Loan document updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        documents.delete()
        return Response({"message": "Loan document deleted successfullly"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def documentTypes(request, id=None):
    if request.method == 'GET':
        if id is None:
            documents = DocumentType.objects.all()
            serializer = LoanDocumentTypeSerializer(documents, many=True)
            return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                document = get_object_or_404(DocumentType, id=id)
                serializer = LoanDocumentTypeSerializer(document)
                return Response({"message": "Success", "result": serializer.data}, status=status.HTTP_200_OK)
            except DocumentType.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        serializer = LoanDocumentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan document type created successfully", "results": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Loan document type creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
# a function got getting and creating loan status
def document_status(request):
    if request.method == 'GET':
        try:
            document_status = DocumentStatus.objects.all()
        except DocumentStatus.DoesNotExist():
            return Response({'Error': 'Document status not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LoanDocumentStatusSerializer(document_status, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = LoanDocumentStatusSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Document status created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Document status creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# a function got getting and creating loan status
def pay_loan(request):
    serializer = LoanRepaymentSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Loan paid successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Loan payment failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
