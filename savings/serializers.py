from rest_framework import serializers
from .models import Savings_Account

class SavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savings_Account
        fields = "__all__"
    