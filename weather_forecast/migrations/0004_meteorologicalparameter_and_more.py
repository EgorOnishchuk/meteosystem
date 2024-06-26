# Generated by Django 5.0.4 on 2024-05-08 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_forecast', '0003_remove_meteorologicalservice_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeteorologicalParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('unit', models.CharField(max_length=20, verbose_name='Единица измерения')),
            ],
        ),
        migrations.AddField(
            model_name='meteorologicalservice',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meteorologicalapi',
            name='key',
            field=models.CharField(max_length=200, verbose_name='Ключ'),
        ),
        migrations.AlterField(
            model_name='meteorologicalapi',
            name='meteorological_service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='weather_forecast.meteorologicalservice', verbose_name='Метеорологическая служба'),
        ),
        migrations.AlterField(
            model_name='meteorologicalapi',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='meteorologicalapi',
            name='url',
            field=models.URLField(verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='meteorologicalservice',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='meteorologicalservice',
            name='foundation_year',
            field=models.PositiveSmallIntegerField(verbose_name='Год основания'),
        ),
        migrations.AlterField(
            model_name='meteorologicalservice',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='meteorologicalservice',
            name='official_url',
            field=models.URLField(unique=True, verbose_name='Официальный URL'),
        ),
        migrations.AddField(
            model_name='meteorologicalservice',
            name='parameters',
            field=models.ManyToManyField(to='weather_forecast.meteorologicalparameter', verbose_name='Параметры'),
        ),
    ]
