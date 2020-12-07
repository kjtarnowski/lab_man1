from django.urls import path
from . import views


app_name = "ml"


urlpatterns = [
    path("add_ml_algorithm/", views.add_algorithm_view, name="add_ml_algorithm"),
    path("edit_ml_algorithm/<int:algorithm_id>", views.edit_algorithm_view, name="edit_ml_algorithm"),
    path("ml_algorithm_list/", views.ml_algorithm_list_view, name="ml_algorithm_list"),
    path("ml_reqest_list/", views.ml_request_list_view, name="ml_request_list")
]
