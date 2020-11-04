from django import forms
from .models import Experiment, Result, Compound


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


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = (
            "compound",
            "experiment_Sp",
            "experiment_Sp",
            "experiment_MLOGP",
            # "result_Sp",
            # "result_HyWi",
            # "result_ARR",
            # "result_GSTS2i",
            # "result_MLOGP",
            # "result_Eta_beta",
            "comments"
        )


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
