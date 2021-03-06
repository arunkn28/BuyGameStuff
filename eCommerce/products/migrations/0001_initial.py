# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-24 17:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('PS4', 'PS4'), ('PS3', 'PS3'), ('PC', 'PC'), ('XBOX1', 'XBOX1')], max_length=10)),
                ('description', models.TextField(max_length=100)),
                ('image', models.ImageField(blank=True, default=None, upload_to='')),
                ('created_by', models.CharField(default=None, max_length=50)),
                ('created_datetime', models.DateTimeField(default=None)),
                ('modified_by', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('modified_datetime', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(default=None, max_length=50)),
                ('name', models.CharField(default=None, max_length=120)),
                ('description', models.TextField(default=None)),
                ('image', models.ImageField(blank=True, default=None, upload_to='')),
                ('featured', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('quntity_per_unit', models.IntegerField(default=None)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('weight', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('units_in_stock', models.IntegerField(default=None)),
                ('created_by', models.CharField(default=None, max_length=50)),
                ('created_datetime', models.DateTimeField(default=None)),
                ('modified_by', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('modified_datetime', models.DateTimeField(blank=True, default=None, null=True)),
                ('category_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
            ],
        ),
    ]
