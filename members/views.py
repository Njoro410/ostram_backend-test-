from rest_framework import generics
from django.core.paginator import Paginator

from .models import Members, Residential_Areas
from .serializers import MemberSerializer, ResidentialAreaSerializer

class MemberList(generics.ListCreateAPIView):
  serializer_class = MemberSerializer

  def get_queryset(self):
    queryset = Members.objects.all()
    # paginator = Paginator(data,25)
    query_param = self.request.query_params.get('q')
    if query_param is not None:
      queryset = queryset.filter(mbr_no=query_param)
    return queryset

class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = MemberSerializer
  queryset = Members.objects.all()

class ResidentialAreaList(generics.ListCreateAPIView):
  serializer_class = ResidentialAreaSerializer
  queryset = Residential_Areas.objects.all()

class ResidentialAreaDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ResidentialAreaSerializer
  queryset = Residential_Areas.objects.all()
