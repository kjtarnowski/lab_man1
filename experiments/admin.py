from django.contrib import admin
from .models import LabPerson, Experiment, Project, Aparat, ExperimentType, \
 Compound, Result, ExperimentalSet


@admin.register(LabPerson)
class LabPersonAdmin(admin.ModelAdmin):
    list_display = ("lab_name", "date_joined", "is_staff", "is_active")
    list_filter = ('lab_name',)
    search_fields = ('lab_name',)


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        "compound",
        "experiment_type",
        "lab_person",
        "experiment_date",
        "experimental_set",
        "created",
        "updated",
        "progress",
        "comments",
        "final"
        )
    list_filter = (
        "compound",
        "experiment_type",
        "experiment_date",
        "experimental_set",
        "lab_person",
        "progress",
        "final"
    )
    search_fields = (
        "compound",
        "experiment_type",
        "experimental_set",
        "lab_person",
        "progress"
        )
    # prepopulated_fields = {"slug": ("compound", "experiment_type")}
    # raw_id_fields = ("author", )
    date_hierarchy = "experiment_date"
    ordering = ("experiment_date", "compound")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "compound",
        "experiment_type",
        "experiment",
        "comments",
        "result1",
        "result2",
        "result3",
        "result4",
        "result5"
        )
    list_filter = (
        "compound",
        "experiment_type",
        "experiment"
        )
    search_fields = (
        "compound",
        "experiment_type",
        "experiment"
        )
    ordering = ("experiment", "compound")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_name",)
    list_filter = ("project_name",)


@admin.register(Aparat)
class AparatAdmin(admin.ModelAdmin):
    list_display = ("aparat_name",)
    list_filter = ("aparat_name",)


@admin.register(ExperimentType)
class ExperimentTypeAdmin(admin.ModelAdmin):
    list_display = ("experiment_name",)
    list_filter = ("experiment_name",)


@admin.register(Compound)
class CompoundTypeAdmin(admin.ModelAdmin):
    list_display = ("compound_name", "compound_mass", "compound_formula", "project", "comments")
    list_filter = ("compound_name",)


@admin.register(ExperimentalSet)
class ExperimentalSetAdmin(admin.ModelAdmin):
    list_display = ("set_name", "experiment_date")
    list_filter = ("set_name",)
