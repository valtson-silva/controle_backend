from rest_framework import serializers
from .models import Exhausts, ExhaustsCarModel, CarModel
        

class ExhaustsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhausts
        fields = "__all__"
        
        
class ExhaustsCarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExhaustsCarModel
        fields = "__all__"
        
        
class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = "__all__"
