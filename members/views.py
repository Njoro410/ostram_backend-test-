from rest_framework import generics

from .models import Members, Residential_Areas
from .serializers import MemberSerializer, ResidentialAreaSerializer

class MemberList(generics.ListCreateAPIView):
  serializer_class = MemberSerializer

  def get_queryset(self):
    queryset = Members.objects.all()
    specific_member = self.request.query_params.get('mbr_no')
    if specific_member is not None:
      queryset = queryset.filter(mbr_no=specific_member)
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
