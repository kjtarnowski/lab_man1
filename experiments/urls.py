from django.urls import path
from . import views


app_name = "experiments"


urlpatterns = [
    path("experimentList/", views.experiments_list, name="experimentList"),
    path("experiment/<int:experiment_id>/", views.edit_experiment, name="editExperiment"),
    path("resultList/", views.results_list, name="resultList"),
    path("compoundList/", views.compound_list, name="compoundList"),
    path("compound/<int:compound_id>/", views.edit_compound, name="editCompound"),
    path("uploadCompound", views.compounds_upload, name="uploadCompound"),
    path("uploadExperiment", views.experiments_upload, name="uploadExperiment"),
]
