from django import forms
from .models import Crop

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = '__all__'
        widgets = {
            'soil_texture': forms.Select(),
            'organic_matter': forms.Select(),
            'drainage_status': forms.Select(),
            'irrigation_type': forms.Select(),
            'sowing_season': forms.Select(),
            'crop_type_preference': forms.Select(),
            'risk_appetite': forms.Select(),
        }
