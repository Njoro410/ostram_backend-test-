from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import MemberSerializer, ResidentialAreaSerializer
from django.http import Http404

class StandardResultSetPagination(PageNumberPagination):
  """
  Returns paginated response
  """
  page_size = 50
  page_size_query_param = 'page_size'
  max_page_size = 1000

class MemberList(generics.ListCreateAPIView):
  """
  GET, POST
  List all members and creates new members. It also finds a member by member_no passed in as a query parameter
  """
  serializer_class = MemberSerializer
  pagination_class = StandardResultSetPagination

  def get_queryset(self):
    try:
      queryset = members.objects.all()
      query_param = self.request.query_params.get('q')
      if query_param is not None:
        queryset = queryset.filter(mbr_no=query_param)
      return queryset

    except:
      raise Http404

class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
  """
  GET, PUT/PATCH, DELETE
  Display individual member and updates with PUT, and deletes member
  """
  serializer_class = MemberSerializer
  queryset = members.objects.all()

# class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
#   serializer_class = MemberSerializer
#   def get_queryset(self):
#     try:
#       members_list = members.objects.all()
#       return members_list
#     except:
#       from django.http import Http404
#       raise Http404('This user does not exist')

class ResidentialAreaList(generics.ListCreateAPIView):
  """
  GET, POST
  List all residential areas and creates new ones.
  """
  serializer_class = ResidentialAreaSerializer
  queryset = residential_areas.objects.all()
  pagination_class = StandardResultSetPagination

class ResidentialAreaDetail(generics.RetrieveUpdateDestroyAPIView):
  """
  GET, PUT/PATCH, DELETE
  Display individual residential area with DELETE and updates with PUT, and deletes residential area with DELETE
  """
  serializer_class = ResidentialAreaSerializer
  queryset = residential_areas.objects.all()
