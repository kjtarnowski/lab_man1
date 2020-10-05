import django_filters
from django_filters import CharFilter

from .models import Experiment


class ExperimentFilter(django_filters.FilterSet):
    compound = CharFilter(field_name='compound__compound_name', lookup_expr='icontains')

    class Meta:
        model = Experiment
        fields = '__all__'
