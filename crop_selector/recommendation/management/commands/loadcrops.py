import csv
from django.core.management.base import BaseCommand
from recommendation.models import CropMaster

class Command(BaseCommand):
    help = 'Load crop master data from crop_master.csv'

    def handle(self, *args, **kwargs):
        with open('crop_master.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                CropMaster.objects.create(
                    name=row['name'],
                    soil_texture=row['soil_texture'],
                    ph_min=row['ph_min'],
                    ph_max=row['ph_max'],
                    organic_matter=row['organic_matter'],
                    drainage=row['drainage'],
                    rainfall_min=row['rainfall_min'],
                    rainfall_max=row['rainfall_max'],
                    temperature_min=row['temperature_min'],
                    temperature_max=row['temperature_max']
                )
            self.stdout.write(self.style.SUCCESS('CropMaster data loaded successfully.'))
