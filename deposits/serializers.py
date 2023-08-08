from rest_framework import serializers
from .models import DepositsAccount, ReceiveDeposits

class DepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositsAccount
        fields = "__all__"
    
class AddDepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiveDeposits
        fields = "__all__"
    
    def save(self, **kwargs):
        user = self.context['request'].user
        kwargs['created_by'] = user
        kwargs['updated_by'] = user
        return super().save(**kwargs)