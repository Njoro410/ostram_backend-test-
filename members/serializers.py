from rest_framework import serializers
from .models import *


class MemberSerializer(serializers.ModelSerializer):
    residential_name = serializers.CharField(source="residential.name", read_only=True)
    residential = serializers.IntegerField(
        source="residential.area_code", read_only=True
    )

    class Meta:
        model = Members
        fields = "__all__"

    # def save(self, **kwargs):
    #     user = self.context["request"].user
    #     kwargs["created_by"] = user
    #     return super().save(**kwargs)


class ResidentialAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialAreas
        fields = "__all__"
