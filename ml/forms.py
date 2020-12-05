from django import forms
from .models import MLAlgorithm


class MLAlgorithmForm(forms.ModelForm):
    class Meta:
        model = MLAlgorithm
        fields = ("name", "description", "version", "joblib_binary_file_algorithm", 'joblib_binary_file_encoders')
        labels = {'joblib_binary_file_algorithm': "Upload joblib file - algorithm",
                  'joblib_binary_file_encoders': "Upload joblib file - encoders"}
        widgets = {
            'joblib_binary_file_algorithm': forms.FileInput(),
            'joblib_binary_file_encoders': forms.FileInput()
        }
