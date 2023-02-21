from rest_framework import serializers
from .models import *

class MemberSerializer(serializers.ModelSerializer):
  class Meta:
    model = members
    fields = ('__all__')

class ResidentialAreaSerializer(serializers.ModelSerializer):
  class Meta:
    model = residential_areas
    fields = ('__all__')