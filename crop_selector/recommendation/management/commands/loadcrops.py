import csv
from django.core.management.base import BaseCommand
from recommendation.models import CropMaster

class Command(BaseCommand):
    help = 'Load crop reference data into CropMaster model'

    def handle(self, *args, **kwargs):
        with open('crop_master.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            CropMaster.objects.all().delete()  # Optional: Clear old data
            count = 0
            for row in reader:
                CropMaster.objects.create(
                    crop_name=row['crop_name'],
                    soil_texture=row['soil_texture'],
                    soil_ph_min=float(row['soil_ph_min']),
                    soil_ph_max=float(row['soil_ph_max']),
                    organic_matter=row['organic_matter'],
                    drainage_status=row['drainage_status'],
                    rainfall_min=float(row['rainfall_min']),
                    rainfall_max=float(row['rainfall_max']),
                    temperature_min=float(row['temperature_min']),
                    temperature_max=float(row['temperature_max']),
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} crop records.'))
