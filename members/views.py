from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Members, Residential_Areas
from .serializers import MemberSerializer, ResidentialAreaSerializer

#pagination
class StandardResultSetPagination(PageNumberPagination):
  page_size = 50
  page_size_query_param = 'page_size'
  max_page_size = 1000
class MemberList(generics.ListCreateAPIView):
  serializer_class = MemberSerializer
  pagination_class = StandardResultSetPagination

  def get_queryset(self):
    # queryset = Members.objects.all()
    queryset = Members.objects.all()
    query_param = self.request.query_params.get('q')
    # data = queryset
    if query_param is not None:
      # queryset = queryset.filter(mbr_no=query_param)
      queryset = queryset.filter(mbr_no=query_param)
      # data = queryset
    return queryset

class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = MemberSerializer
  queryset = Members.objects.all()

class ResidentialAreaList(generics.ListCreateAPIView):
  serializer_class = ResidentialAreaSerializer
  queryset = Residential_Areas.objects.all()
  pagination_class = StandardResultSetPagination

class ResidentialAreaDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ResidentialAreaSerializer
  queryset = Residential_Areas.objects.all()
