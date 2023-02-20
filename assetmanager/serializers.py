from rest_framework import serializers
from .models import loanAsset,assetDocument
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = loanAsset
        fields = "__all__"
        
class AssetDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = assetDocument
        fields = "__all__"