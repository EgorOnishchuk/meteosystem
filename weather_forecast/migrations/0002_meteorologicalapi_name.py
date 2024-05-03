# Generated by Django 5.0.4 on 2024-04-08 13:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_forecast', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meteorologicalapi',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]