"""lab_man1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.views.generic.base import TemplateView
from django.urls import path, include
from rest_framework.schemas import get_schema_view

from ml.api_views import PredictView
from .api import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("experiments/", include("experiments.urls", namespace="experiments")),
    path("ml/", include("ml.urls", namespace="ml")),
    path("api/v1/", include(router.urls)),
    path("api/v1/predict/<str:algorithm_name>/<str:algorithm_version>", PredictView.as_view(), name="predict"),
    path("api/v1/rest-auth/", include("rest_auth.urls")),
    path(
        "openapi/",
        get_schema_view(title="Lab Experiments management app", description="API for experiments app"),
        name="openapi-schema",
    ),
    path(
        "docs/",
        TemplateView.as_view(template_name="documentation.html", extra_context={"schema_url": "openapi-schema"}),
        name="swagger-ui",
    ),
]
