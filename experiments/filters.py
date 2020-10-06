import django_filters
from django_filters import CharFilter

from .models import Experiment, Result


class ExperimentFilter(django_filters.FilterSet):
    compound = CharFilter(field_name='compound__compound_name', lookup_expr='icontains')
    comments = CharFilter(field_name='comments', lookup_expr='icontains')

    class Meta:
        model = Experiment
        fields = '__all__'


class ResultFilter(django_filters.FilterSet):
    compound = CharFilter(field_name='compound__compound_name', lookup_expr='icontains')
    comments = CharFilter(field_name='comments', lookup_expr='icontains')

    class Meta:
        model = Result
        fields = ["compound", "experiment_type", "experiment", "comments"]