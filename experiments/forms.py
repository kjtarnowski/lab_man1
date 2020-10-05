from django import forms
from .models import Experiment


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ("compound", "experiment_type", "lab_person", "experiment_date", "progress", "comments", "final", "result1", "result2", "result3")

