from django.contrib import admin
from .models import LabPerson, Experiment, Project, Aparat,  \
 Compound, Result, ExperimentalSet, Experiment_Sp, Experiment_ARR


@admin.register(LabPerson)
class LabPersonAdmin(admin.ModelAdmin):
    list_display = ("lab_name", "date_joined", "is_staff", "is_active")
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
    list_display = ("project_name",)
    list_filter = ("project_name",)


@admin.register(Aparat)
class AparatAdmin(admin.ModelAdmin):
    list_display = ("aparat_name",)
    list_filter = ("aparat_name",)


# @admin.register(ExperimentType)
# class ExperimentTypeAdmin(admin.ModelAdmin):
#     list_display = ("experiment_name",)
#     list_filter = ("experiment_name",)


@admin.register(Compound)
class CompoundTypeAdmin(admin.ModelAdmin):
    list_display = ("compound_name", "compound_mass", "compound_formula", "project", "comments")
    list_filter = ("compound_name",)


@admin.register(ExperimentalSet)
class ExperimentalSetAdmin(admin.ModelAdmin):
    list_display = ("set_name", "experiment_date")
    list_filter = ("set_name",)


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
    # prepopulated_fields = {"slug": ("compound", "experiment_type")}
    # raw_id_fields = ("author", )
    date_hierarchy = "experiment_date"
    ordering = ("experiment_date", "compound")