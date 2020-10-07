from django import forms
from .models import Experiment, Result, Compound


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = (
            "compound",
            "experiment_type",
            "lab_person",
            "experiment_date",
            "experimental_set",
            "progress",
            "comments",
            "final"
        )
    experiment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datetime-input'}))


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


class CompoundForm(forms.ModelForm):
    class Meta:
        model = Compound
        fields = (
            "compound_name",
            "compound_mass",
            "compound_monoisotopic_mass",
            "compound_formula",
            "comments"
        )
