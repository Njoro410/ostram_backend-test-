from rest_framework import serializers
from .models import Members, Residential_Areas

class MemberSerializer(serializers.ModelSerializer):
  class Meta:
    model = Members
    fields = ('__all__')

class ResidentialAreaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Residential_Areas
    fields = ('__all__')