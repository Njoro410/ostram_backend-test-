from django.shortcuts import render
from .models import Loans, Loan_Type, Documents, documentType
from .serializers import LoanTypeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


@api_view(['GET', 'POST'])
def loantypes(request):
    """
    list and add loan types
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