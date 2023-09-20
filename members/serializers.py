from rest_framework import serializers
from .models import *


class MemberSerializer(serializers.ModelSerializer):
    residential_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Members
        fields = ('__all__')
        
        
    def get_residential_name(self,member):
        if member.residential:
            residential = member.residential.name
            return residential
        return None

    # def save(self, **kwargs):
    #     user = self.context["request"].user
    #     kwargs["created_by"] = user
    #     return super().save(**kwargs)


class ResidentialAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialAreas
        fields = "__all__"
