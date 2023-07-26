from rest_framework import serializers
from .models import DailyContributions

class DailyContributionsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = DailyContributions
        fields = "__all__"
        