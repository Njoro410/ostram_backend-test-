from django.shortcuts import render
from .models import Loans, Loan_Type, Documents, documentType, Loan_Status
from .serializers import LoanTypeSerializer, LoanSerializer, LoanDocumentSerializer,LoanStatusSerializer, LoanDocumentTypeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from members.models import members
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
        loantype = Loan_Type.objects.get(id=id)
    except Loan_Type.DoesNotExist:
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
            loan_status = Loan_Status.objects.all()
        except Loan_Status.DoesNotExist():
            return Response({'Error': 'Loan status not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LoanStatusSerializer(loan_status, many=True)
        return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = LoanStatusSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan status created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Loan status creation failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
#  a function to get a list of all loans
def get_all_loans(request):
    loans = Loans.objects.all()
    if not loans:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = LoanSerializer(loans, many=True)
    return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
# get loans based on member no
def get_loans_by_member_no(request, member_no):
    try:
        member = get_object_or_404(members, mbr_no=member_no)
        loan = Loans.objects.filter(lendee=member)
    except Loans.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LoanSerializer(loan, many=True)
        return Response({"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = LoanSerializer(loan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Loan updated successfully", "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({"message": "Loan updating failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
            serializer.save(loan=loan)
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
            documents = documentType.objects.all()
            serializer = LoanDocumentTypeSerializer(documents, many=True)
            return Response({"message": "Success", "results": serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                document = get_object_or_404(documentType, id=id)
                serializer = LoanDocumentTypeSerializer(document)
                return Response({"message": "Success", "result": serializer.data}, status=status.HTTP_200_OK)
            except documentType.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    

