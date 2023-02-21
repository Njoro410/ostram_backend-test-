from rest_framework import serializers
from .models import Deposits_Account

class DepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposits_Account
        fields = "__all__"
    