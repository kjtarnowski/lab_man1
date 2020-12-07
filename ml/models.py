from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User


class MLAlgorithm(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    version = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    joblib_binary_file_algorithm = models.BinaryField(blank=True, null=True, default=None, editable=True)
    joblib_binary_file_encoders = models.BinaryField(blank=True, null=True, default=None, editable=True)

    def __str__(self):
        return self.name


class MLRequest(models.Model):
    input_data = models.CharField(max_length=10000)
    full_response = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    mlalgorithm = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self. mlalgorithm.name}_{self.created_at.strftime('%m/%d/%Y, %H:%M:%S')}"
