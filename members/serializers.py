from rest_framework import serializers
from .models import *



class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = members
        fields = ('__all__')

    def save(self, **kwargs):
        user = self.context['request'].user
        kwargs['created_by'] = user
        return super().save(**kwargs)


class ResidentialAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = residential_areas
        fields = ('__all__')
