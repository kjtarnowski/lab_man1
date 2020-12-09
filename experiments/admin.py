from django.contrib import admin
from .models import LabPerson, Experiment, Project, Aparat, Compound, ExperimentalSet, ExperimentType


@admin.register(LabPerson)
class LabPersonAdmin(admin.ModelAdmin):
    list_display = ("lab_name",)
    list_filter = ("lab_name",)
    search_fields = ("lab_name",)


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        "compound",
        "lab_person",
        "experiment_date",
        "experimental_set",
        "created",
        "updated",
        "progress",
        "comments",
        "final",
        "exptype",
        "experimental_results",
    )
    search_fields = ("compound", "experimental_set", "lab_person", "progress")
    date_hierarchy = "experiment_date"
    ordering = ("experiment_date", "compound")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)


@admin.register(Aparat)
class AparatAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)


@admin.register(Compound)
class CompoundTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "mass", "formula", "project", "comments", "smiles")
    list_filter = ("project",)


@admin.register(ExperimentalSet)
class ExperimentalSetAdmin(admin.ModelAdmin):
    list_display = ("name", "experiment_date")


@admin.register(ExperimentType)
class ExperimentTypeSetAdmin(admin.ModelAdmin):
    list_display = ("name",)

