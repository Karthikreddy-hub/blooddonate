# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-12-22 16:39
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BloodData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('email', models.EmailField(max_length=100)),
                ('mobile', models.BigIntegerField()),
                ('location', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('bloodgroups', multiselectfield.db.fields.MultiSelectField(choices=[('A-', 'A NAGATIVE'), ('A+', 'A POSITIVE'), ('B-', 'B NAGATIVE'), ('B+', 'B POSITIVE'), ('AB-', 'AB NAGATIVE'), ('AB+', 'AB POSITIVE'), ('O-', 'O NAGATIVE'), ('O+', 'O POSITIVE')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Login_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Register_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('mobile', models.BigIntegerField()),
                ('password1', models.CharField(max_length=100)),
                ('password2', models.CharField(max_length=100)),
            ],
        ),
    ]