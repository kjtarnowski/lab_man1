# Generated by Django 2.2 on 2020-12-05 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MLAlgorithm",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=128)),
                ("description", models.CharField(max_length=1000)),
                ("version", models.CharField(max_length=128)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("joblib_binary_file", models.BinaryField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="MLRequest",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("input_data", models.CharField(max_length=10000)),
                ("full_response", models.CharField(max_length=10000)),
                ("response", models.CharField(max_length=10000)),
                ("feedback", models.CharField(blank=True, max_length=10000, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("mlalgorithm", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="ml.MLAlgorithm")),
            ],
        ),
    ]
