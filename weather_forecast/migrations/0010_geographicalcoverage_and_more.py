# Generated by Django 5.0.4 on 2024-05-16 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_forecast', '0009_remove_weathertime_meteorological_service_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeographicalCoverage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Географическое покрытие',
                'verbose_name_plural': 'Географическое покрытие',
            },
        ),
        migrations.AlterField(
            model_name='meteorologicalservice',
            name='description',
            field=models.TextField(unique=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='meteorologicalservice',
            name='geographical_coverage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='weather_forecast.geographicalcoverage', verbose_name='Географическое покрытие'),
        ),
    ]