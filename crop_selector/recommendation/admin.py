from django.contrib import admin
from .models import Crop, CropMaster

# Crop Admin
@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'soil_texture', 'soil_ph', 'organic_matter',
        'drainage_status', 'rainfall_mm', 'avg_temperature',
        'sowing_season', 'previous_crop', 'district',
        'field_size', 'irrigation_type', 'submitted_at',
    )
    search_fields = ('user__username', 'district', 'village', 'previous_crop')


# CropMaster Admin
@admin.register(CropMaster)
class CropMasterAdmin(admin.ModelAdmin):
    list_display = (
        'crop_name',              # ✅ correct field
        'soil_texture',
        'soil_ph_min',            # ✅ correct field
        'soil_ph_max',            # ✅ correct field
        'organic_matter',
        'drainage_status',        # ✅ correct field
        'rainfall_min',
        'rainfall_max',
        'temperature_min',
        'temperature_max',
    )
    search_fields = ('crop_name',)
