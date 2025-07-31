# crop_selector/recommendation/management/commands/loadcrops.py
import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from recommendation.models import CropMaster

class Command(BaseCommand):
    help = 'Load crop reference data into CropMaster model'

    def handle(self, *args, **kwargs):
        # Look for CSV file in the project root directory
        csv_path = os.path.join(settings.BASE_DIR, 'crop_master.csv')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at: {csv_path}'))
            return
            
        try:
            with open(csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                # Clear existing data
                CropMaster.objects.all().delete()
                self.stdout.write(self.style.WARNING('Cleared existing crop data.'))
                
                count = 0
                errors = 0
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 because row 1 is header
                    try:
                        # Debug: Print first few rows
                        if count < 3:
                            self.stdout.write(f"Processing row {row_num}: {row}")
                        
                        crop = CropMaster.objects.create(
                            crop_name=row['crop_name'].strip(),
                            soil_texture=row['soil_texture'].strip(),
                            soil_ph_min=float(row['soil_ph_min']),
                            soil_ph_max=float(row['soil_ph_max']),
                            organic_matter=row['organic_matter'].strip(),  # Keep as string
                            drainage_status=row['drainage_status'].strip(),  # Fixed field name
                            rainfall_min=float(row['rainfall_min']),
                            rainfall_max=float(row['rainfall_max']),
                            temperature_min=float(row['temperature_min']),
                            temperature_max=float(row['temperature_max']),
                        )
                        count += 1
                        
                    except Exception as e:
                        errors += 1
                        self.stdout.write(
                            self.style.ERROR(f'Error processing row {row_num}: {e}')
                        )
                        if errors > 10:  # Stop if too many errors
                            self.stdout.write(self.style.ERROR('Too many errors, stopping.'))
                            break
                
                if count > 0:
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully loaded {count} crop records.')
                    )
                    
                    # Show sample data
                    sample_crops = CropMaster.objects.all()[:5]
                    self.stdout.write("\n📋 Sample loaded data:")
                    for crop in sample_crops:
                        self.stdout.write(f"  - {crop.crop_name}: {crop.soil_texture}, pH {crop.soil_ph_min}-{crop.soil_ph_max}")
                else:
                    self.stdout.write(self.style.ERROR('No records were loaded.'))
                    
                if errors > 0:
                    self.stdout.write(self.style.WARNING(f'Encountered {errors} errors during loading.'))
                    
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to CSV file (default: crop_master.csv in project root)',
        )