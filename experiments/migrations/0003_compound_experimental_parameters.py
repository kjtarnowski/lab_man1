# Generated by Django 2.2 on 2020-11-05 14:53

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiments', '0002_auto_20201104_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='compound',
            name='experimental_parameters',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]