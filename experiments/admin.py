from django.contrib import admin
from .models import LabPerson, Experiment, Project, Aparat,  \
 Compound, ExperimentalSet, ExperimentType


@admin.register(LabPerson)
class LabPersonAdmin(admin.ModelAdmin):
    list_display = ("lab_name", )
    list_filter = ('lab_name',)
    search_fields = ('lab_name',)


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
        "experimental_results"
        )
    list_filter = (
        "compound",
        "experiment_date",
        "experimental_set",
        "lab_person",
        "progress",
        "final",
        "exptype"
    )
    search_fields = (
        "compound",
        "experimental_set",
        "lab_person",
        "progress"
        )
    # prepopulated_fields = {"slug": ("compound", "experiment_type")}
    # raw_id_fields = ("author", )
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


# @admin.register(ExperimentType)
# class ExperimentTypeAdmin(admin.ModelAdmin):
#     list_display = ("experiment_name",)
#     list_filter = ("experiment_name",)


@admin.register(Compound)
class CompoundTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "mass", "formula", "project", "comments")
    list_filter = ("name",)


@admin.register(ExperimentalSet)
class ExperimentalSetAdmin(admin.ModelAdmin):
    list_display = ("name", "experiment_date")
    list_filter = ("name",)


@admin.register(ExperimentType)
class ExperimentTypeSetAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)

