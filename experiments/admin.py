from django.contrib import admin
from .models import LabPerson, Experiment, Project, Aparat,  \
 Compound, Result, ExperimentalSet, Experiment_Sp, Experiment_ARR


@admin.register(LabPerson)
class LabPersonAdmin(admin.ModelAdmin):
    list_display = ("name", "date_joined", "is_staff", "is_active")
    list_filter = ('name',)
    search_fields = ('name',)


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
        "final"
        )
    list_filter = (
        "compound",
        "experiment_date",
        "experimental_set",
        "lab_person",
        "progress",
        "final"
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


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "compound",
        "experiment_Sp",
        "experiment_ARR",
        "experiment_MLOGP",
        # "result_Sp",
        # "result_HyWi",
        # "result_ARR",
        # "result_GSTS2i",
        # "result_MLOGP",
        # "result_Eta_beta",
        "comments",
        )
    search_fields = (
        "compound",
        )


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


@admin.register(Experiment_Sp)
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
        "result_Sp",
        "result_HyWi"
        )
    list_filter = (
        "compound",
        "experiment_date",
        "experimental_set",
        "lab_person",
        "progress",
        "final"
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


@admin.register(Experiment_ARR)
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
        "result_ARR",
        "result_GSTS2i"
        )
    list_filter = (
        "compound",
        "experiment_date",
        "experimental_set",
        "lab_person",
        "progress",
        "final"
    )
    search_fields = (
        "compound",
        "experimental_set",
        "lab_person",
        "progress"
        )
    date_hierarchy = "experiment_date"
    ordering = ("experiment_date", "compound")
