from django import forms
from .models import Experiment, Result


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = (
            "compound",
            "experiment_type",
            "lab_person",
            "experiment_date",
            "progress",
            "comments",
            "final"
        )


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = (
            "compound",
            "experiment_type",
            "experiment",
            "comments",
            "result1",
            "result2",
            "result3",
            "result4",
            "result5",
        )
