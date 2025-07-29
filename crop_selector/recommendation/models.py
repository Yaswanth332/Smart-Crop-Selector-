from django.db import models

# Crop model to store crop details
class Crop(models.Model):
    SOIL_TEXTURE_CHOICES = [
        ('Loam', 'Loam'),
        ('Clay', 'Clay'),
        ('Sandy', 'Sandy'),
        ('Clay Loam', 'Clay Loam'),
        ('Sandy Loam', 'Sandy Loam'),
    ]
    DRAINAGE_CHOICES = [
        ('Well-drained', 'Well-drained'),
        ('Moderately drained', 'Moderately drained'),
        ('Poorly drained', 'Poorly drained'),
    ]
    ORGANIC_MATTER_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    soil_texture = models.CharField(max_length=50, choices=SOIL_TEXTURE_CHOICES)
    soil_ph = models.FloatField()
    organic_matter = models.CharField(max_length=10, choices=ORGANIC_MATTER_CHOICES)
    drainage_status = models.CharField(max_length=20, choices=DRAINAGE_CHOICES)
    soil_salinity = models.BooleanField(default=False)

    rainfall_mm = models.FloatField()
    avg_temperature = models.FloatField()
    humidity_level = models.IntegerField(null=True, blank=True)
    frost_risk = models.BooleanField(default=False)

    IRRIGATION_CHOICES = [
        ('Canal', 'Canal'),
        ('Borewell', 'Borewell'),
        ('Rainfed', 'Rainfed'),
        ('None', 'None'),
    ]
    irrigation_type = models.CharField(max_length=20, choices=IRRIGATION_CHOICES)
    water_holding_capacity = models.FloatField(null=True, blank=True)
    field_size = models.FloatField(help_text="In acres or hectares")

    SEASON_CHOICES = [
        ('Kharif', 'Kharif'),
        ('Rabi', 'Rabi'),
        ('Zaid', 'Zaid'),
    ]
    CATEGORY_CHOICES = [
        ('Cereal', 'Cereal'),
        ('Pulse', 'Pulse'),
        ('Oilseed', 'Oilseed'),
        ('Vegetable', 'Vegetable'),
        ('Fruit', 'Fruit'),
    ]
    sowing_season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    previous_crop = models.CharField(max_length=50)
    crop_type_preference = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)

    district = models.CharField(max_length=50)
    village = models.CharField(max_length=50, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    market_access = models.CharField(max_length=100, null=True, blank=True)
    mechanized = models.BooleanField(default=False)
    risk_appetite = models.CharField(
        max_length=50,
        choices=[('Stable', 'Stable'), ('High-Profit', 'High-Profit')],
        null=True, blank=True
    )
    language_preference = models.CharField(max_length=20, null=True, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.district} | {self.soil_texture} | {self.sowing_season}"


class CropMaster(models.Model):
    name = models.CharField(max_length=100, unique=True)
    soil_texture = models.CharField(max_length=50, choices=Crop.SOIL_TEXTURE_CHOICES)
    ph_min = models.FloatField()
    ph_max = models.FloatField()
    organic_matter = models.CharField(max_length=10, choices=Crop.ORGANIC_MATTER_CHOICES)
    drainage = models.CharField(max_length=30, choices=Crop.DRAINAGE_CHOICES)

    rainfall_min = models.FloatField()
    rainfall_max = models.FloatField()
    temperature_min = models.FloatField()
    temperature_max = models.FloatField()

    def __str__(self):
        return self.name
