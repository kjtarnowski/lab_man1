from django import forms
from .models import Experiment, Compound


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = (
            "compound",
            "lab_person",
            "experiment_date",
            "experimental_set",
            "progress",
            "comments",
            "final"
        )
    experiment_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'datetime-input'
        }))


class CompoundForm(forms.ModelForm):
    class Meta:
        model = Compound
        fields = (
            "name",
            "mass",
            "monoisotopic_mass",
            "formula",
            "comments"
        )
