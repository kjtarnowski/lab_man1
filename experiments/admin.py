from django.contrib import admin
from .models import LabPerson, Experiment, Project, Aparat, ExperimentType, Compound


@admin.register(LabPerson)
class LabPersonAdmin(admin.ModelAdmin):
    list_display = ("lab_name", "date_joined", "is_staff", "is_active")
    list_filter = ('lab_name',)
    search_fields = ('lab_name',)


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ("compound", "experiment_type", "lab_person", "appointed", "created", "updated", "progress", "comments", "final", "result1", "result2", "result3")
    list_filter = ("compound", "experiment_type", "lab_person", "progress", "final")
    search_fields = ("compound", "experiment_type", "lab_person",  "progress", "final")
    # prepopulated_fields = {"slug": ("compound", "experiment_type")}
    # raw_id_fields = ("author", )
    date_hierarchy = "appointed"
    ordering = ("appointed", "compound")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_name",)
    list_filter = ("project_name",)
    prepopulated_fields = {"slug": ("project_name", )}


@admin.register(Aparat)
class AparatAdmin(admin.ModelAdmin):
    list_display = ("aparat_name",)
    list_filter = ("aparat_name",)
    prepopulated_fields = {"slug": ("aparat_name", )}


@admin.register(ExperimentType)
class ExperimentTypeAdmin(admin.ModelAdmin):
    list_display = ("experiment_name",)
    list_filter = ("experiment_name",)
    prepopulated_fields = {"slug": ("experiment_name", )}


@admin.register(Compound)
class CompoundTypeAdmin(admin.ModelAdmin):
    list_display = ("compound_name",)
    list_filter = ("compound_name",)
    prepopulated_fields = {"slug": ("compound_name", )}
