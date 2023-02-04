from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SavingsSerializer
from rest_framework import status
from .models import Savings_Account
from django.db.models import Sum
# Create your views here.

@api_view(['GET'])
def get_total_savings(request):
    total_savings = Savings_Account.objects.all().aggregate(Sum('balance'))['balance__sum']
    return Response({'total_savings': total_savings}, status=status.HTTP_200_OK)