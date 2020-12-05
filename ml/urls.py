from django.urls import path
from . import views


app_name = "ml"


urlpatterns = [
    path("add_ml_algorithm", views.add_algorithm, name="add_ml_algorithm"),
]
