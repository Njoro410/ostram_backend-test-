from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SavingsSerializer
from rest_framework import status
from .models import Savings_Account
from members.models import Members
from django.db.models import Sum
# Create your views here.


@api_view(['GET'])
def get_total_savings(request):
    total_savings = Savings_Account.objects.all().aggregate(Sum('balance'))[
        'balance__sum']
    return Response({'total_savings': total_savings}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
# get savings based on member number
def get_member_savings(request, member_no):
    try:
        member = get_object_or_404(Members, mbr_no=member_no)
        savings = Savings_Account.objects.filter(account_owner=member)
    except Savings_Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SavingsSerializer(savings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = SavingsSerializer(savings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        savings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
