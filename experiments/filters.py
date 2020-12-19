import django_filters
from django_filters import CharFilter, FilterSet

from experiments.models import Experiment, Compound


class ExperimentFilter(FilterSet):
    compound = CharFilter(field_name="compound__name", lookup_expr="icontains")
    comments = CharFilter(field_name="comments", lookup_expr="icontains")

    class Meta:
        model = Experiment
        fields = [
            "compound",
            "lab_person",
            "experiment_date",
            "experimental_set",
            "progress",
            "comments",
            "final",
            "exptype",
        ]


class CompoundFilter(FilterSet):
    comments = CharFilter(field_name="comments", lookup_expr="icontains")
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Compound
        fields = ["name", "comments"]
