# Generated migration - replace the content of your newest migration file with this

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0003_alter_crop_field_size'),  # Update this to your latest migration
    ]

    operations = [
        # Drop the old CropMaster table completely
        migrations.RunSQL("DROP TABLE IF EXISTS recommendation_cropmaster;"),
        
        # Create the new CropMaster table with correct structure
        migrations.CreateModel(
            name='CropMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_name', models.CharField(max_length=100)),
                ('soil_texture', models.CharField(max_length=100)),
                ('soil_ph_min', models.FloatField()),
                ('soil_ph_max', models.FloatField()),
                ('organic_matter', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=10)),
                ('drainage_status', models.CharField(max_length=100)),
                ('rainfall_min', models.FloatField()),
                ('rainfall_max', models.FloatField()),
                ('temperature_min', models.FloatField()),
                ('temperature_max', models.FloatField()),
            ],
            options={
                'verbose_name': 'Crop Master',
                'verbose_name_plural': 'Crop Masters',
            },
        ),
    ]