from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import *
from .serializers import MemberSerializer, ResidentialAreaSerializer
from django.http import Http404
#pagination
class StandardResultSetPagination(PageNumberPagination):
  page_size = 50
  page_size_query_param = 'page_size'
  max_page_size = 1000
class MemberList(generics.ListCreateAPIView):
  serializer_class = MemberSerializer
  pagination_class = StandardResultSetPagination

  def get_queryset(self):
    try:

      # queryset = Members.objects.all()
      queryset = members.objects.all()
      query_param = self.request.query_params.get('q')
      # data = queryset
      if query_param is not None:
        # queryset = queryset.filter(mbr_no=query_param)
        queryset = queryset.filter(mbr_no=query_param)
        # data = queryset
      return queryset

    except:
      raise Http404

class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = MemberSerializer
  queryset = members.objects.all()

class ResidentialAreaList(generics.ListCreateAPIView):
  serializer_class = ResidentialAreaSerializer
  queryset = residential_areas.objects.all()
  pagination_class = StandardResultSetPagination

class ResidentialAreaDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ResidentialAreaSerializer
  queryset = residential_areas.objects.all()
