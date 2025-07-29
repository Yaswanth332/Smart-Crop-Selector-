from django.contrib import admin
from .models import Crop, CropMaster

class CropAdmin(admin.ModelAdmin):
    list_display = ('user', 'soil_type', 'ph', 'created_at')  # add more as needed
    search_fields = ('user__username', 'soil_type')

admin.site.register(Crop, CropAdmin)
