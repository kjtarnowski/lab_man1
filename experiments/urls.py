from django.urls import path
from . import views


app_name = 'experiments'


urlpatterns = [
    path('experimentList/', views.experiments_list, name='experimentList'),
]
