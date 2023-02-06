from django.shortcuts import render
from .models import Loans, Loan_Type, Documents, documentType
from .serializers import LoanTypeSerializer, LoanSerializer, LoanDocumentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from members.models import Members
from django.shortcuts import get_object_or_404
# Create your views here.


@api_view(['GET', 'POST'])
def loan_types_get_add(request):
    """
    function to list and add loan types
    """
    if request.method == 'GET':
        types = Loan_Type.objects.all()
        serializer = LoanTypeSerializer(types, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LoanTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def loantype_detail(request, id):
    """
    Retrieve, update or delete a loan type.
    """
    try:
        loantype = Loan_Type.objects.get(id=id)
    except Loan_Type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LoanTypeSerializer(loantype)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LoanTypeSerializer(loantype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        loantype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
#  a function to get a list of all loans
def get_all_loans(request):
    loans = Loans.objects.all()
    if not loans:
        return Response({'detail':'Not found'},status=status.HTTP_404_NOT_FOUND)
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
# get loans based on member no
def get_loans_by_member_no(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        loan = Loans.objects.filter(lendee=member)
    except Loans.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LoanSerializer(loan, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LoanSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def loan_documents_by_loan_id(request, loan_id):
    try:
        loan = get_object_or_404(Loans, id=loan_id)
        documents = Documents.objects.filter(loan=loan)
    except Loans.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LoanDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LoanDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(loan=loan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = LoanDocumentSerializer(documents, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        documents.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
