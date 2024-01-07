from rest_framework import serializers
from .models import DepositsAccount, ReceiveDeposits, WithdrawDeposits


class DepositsSerializer(serializers.ModelSerializer):
    names = serializers.SerializerMethodField()
    mbr_no = serializers.SerializerMethodField()

    def get_names(self, account):
        if account.account_owner:
            owner = account.account_owner.names
            return owner
        return None

    def get_mbr_no(self, account):
        if account.account_owner:
            mbr_no = account.account_owner.mbr_no
            return mbr_no
        return None

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


class WithdrawDepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawDeposits
        fields = "__all__"

    def save(self, **kwargs):
        user = self.context['request'].user
        kwargs['created_by'] = user
        kwargs['updated_by'] = user
        return super().save(**kwargs)


class DepositsReceivedSerializer(serializers.Serializer):
    all_received_deposits = AddDepositsSerializer(many=True)
    monthly_deposits_totals = serializers.ListField(
        child=serializers.DictField())


class WithdrawalsSerializer(serializers.Serializer):
    all_withdrawals = WithdrawDepositsSerializer(many=True)
    monthly_withdrawals_totals = serializers.ListField(
        child=serializers.DictField())
