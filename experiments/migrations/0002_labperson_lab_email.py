# Generated by Django 2.2 on 2020-11-26 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="labperson",
            name="lab_email",
            field=models.EmailField(blank=True, default=None, max_length=254, null=True),
        ),
    ]
