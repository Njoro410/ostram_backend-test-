from rest_framework import serializers
from .models import DepositsAccount

class DepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositsAccount
        fields = "__all__"
    