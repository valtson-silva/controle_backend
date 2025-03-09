from rest_framework import serializers
from .models import MiscellaneousProducts

class MiscellaneousProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiscellaneousProducts
        fields = "__all__"
