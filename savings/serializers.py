from rest_framework import serializers
from .models import SavingsAccount, ReceiveSavings, WithdrawSavings

class SavingsSerializer(serializers.ModelSerializer):
    names = serializers.SerializerMethodField()
    mbr_no = serializers.SerializerMethodField()

    def get_names(self, account):
        if account.account_owner:
            owner = account.account_owner.names
            return owner
        return None
    
    def get_mbr_no(self,account):
        if account.account_owner:
            mbr_no = account.account_owner.mbr_no
            return mbr_no 
        return None
    
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
    
    
class SavingsReceivedSerializer(serializers.Serializer):
    all_received_savings = AddSavingsSerializer(many=True) 
    monthly_savings_totals = serializers.ListField(child=serializers.DictField())
    
    
    
class WithdrawSavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawSavings
        fields = "__all__"
    
    def save(self, **kwargs):
        user = self.context['request'].user
        kwargs['created_by'] = user
        kwargs['updated_by'] = user
        return super().save(**kwargs)
    

    
    
class WithdrawalsSerializer(serializers.Serializer):
    all_withdrawals = WithdrawSavingsSerializer(many=True)
    monthly_withdrawals_totals = serializers.ListField(child=serializers.DictField())