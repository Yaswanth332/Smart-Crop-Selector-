# recommendation/serializers.py
from rest_framework import serializers
from .models import Crop, CropMaster

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'

# Fixed: Added CropMasterSerializer
class CropMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropMaster
        fields = '__all__'