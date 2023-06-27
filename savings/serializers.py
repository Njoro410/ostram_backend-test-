from rest_framework import serializers
from .models import SavingsAccount, ReceiveSavings

class SavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsAccount
        fields = "__all__"
    
class AddSavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiveSavings
        fields = "__all__"
    
    def save(self, **kwargs):
        user = self.context['request'].user
        kwargs['created_by'] = user
        kwargs['updated_by'] = user
        return super().save(**kwargs)