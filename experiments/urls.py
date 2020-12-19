from django.urls import path

from experiments import views


app_name = "experiments"


urlpatterns = [
    path("experimentList/", views.experiments_list_view, name="experimentList"),
    path("experiment/<int:experiment_id>/", views.edit_experiment_view, name="editExperiment"),
    path("resultList/", views.results_list_view, name="resultList"),
    path("compoundList/", views.compound_list_view, name="compoundList"),
    path("compound/<int:compound_id>/", views.edit_compound_view, name="editCompound"),
    path("uploadCompound/", views.compounds_upload_view, name="uploadCompound"),
    path("uploadExperiment/", views.experiments_upload_view, name="uploadExperiment"),
]
