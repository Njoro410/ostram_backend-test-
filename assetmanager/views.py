from django.shortcuts import render
from .models import Asset,assetDocument
from .serializers import AssetSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
# Create your views here.


# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def 