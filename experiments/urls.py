from django.urls import path
from . import views


app_name = 'experiments'


urlpatterns = [
    path('experimentList/', views.experiments_list, name='experimentList'),
    path('<int:experiment_id>/', views.edit_experiment, name='editExperiment'),
]
