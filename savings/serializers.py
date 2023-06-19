from rest_framework import serializers
from .models import SavingsAccount

class SavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsAccount
        fields = "__all__"
    