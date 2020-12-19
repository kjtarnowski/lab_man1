from django.contrib import admin

from ml.models import MLAlgorithm, MLRequest


@admin.register(MLAlgorithm)
class MLAlgorithmAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "version")


@admin.register(MLRequest)
class MLRequestAdmin(admin.ModelAdmin):
    list_display = ("input_data", "full_response", "response", "mlalgorithm")
