from rest_framework import serializers
from .models import loanAsset, assetDocument


class AssetDocumentSerializer(serializers.ModelSerializer):
    proof_of = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    
    def get_proof_of(self,asset):
        _asset = asset.proof_of.name
        name = asset.proof_of.loan.lendee.names
        return f"{name}'s {_asset}"

    def get_created_by(self, asset_creator):
        name = asset_creator.created_by.fullname
        return name

    def get_updated_by(self, asset_updator):
        name = asset_updator.updated_by.fullname
        return name
    class Meta:
        model = assetDocument
        fields = "__all__"


class AssetSerializer(serializers.ModelSerializer):
    loan = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_loan(self, loan):
        _loan = loan.loan.lendee.names
        return _loan

    def get_created_by(self, asset_creator):
        name = asset_creator.created_by.fullname
        return name

    def get_updated_by(self, asset_updator):
        name = asset_updator.updated_by.fullname
        return name

    class Meta:
        model = loanAsset
        fields = "__all__"
