# import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.urls import reverse

from .managers import LabPersonManager


class LabPerson(AbstractBaseUser, PermissionsMixin):
    lab_name = models.CharField(max_length=50, unique=True)
    lab_email = models.EmailField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'lab_name'
    REQUIRED_FIELDS = ['lab_email']

    objects = LabPersonManager()


class Project(models.Model):
    project_name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.project_name


class Aparat(models.Model):
    aparat_name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.aparat_name


class ExperimentType(models.Model):
    experiment_name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.experiment_name


class Compound(models.Model):
    compound_name = models.CharField(max_length=25)
    compound_mass = models.FloatField()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='compounds')
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.compound_name


class Experiment(models.Model):
    PROGRESS_CHOICES = (
        ("TBD", "TBD"),
        ("ONGOING", "ONGOING"),
        ("UC", "UC"),
        ("TO_REP", "TO_REP")
    )
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comments = models.TextField(default="-")
    experiment_date = models.DateField(default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    compound = models.ForeignKey(
        Compound, on_delete=models.CASCADE, related_name='experiments_for_compounds')
    experiment_type = models.ForeignKey(
        ExperimentType, on_delete=models.CASCADE, related_name='experiments_of_this_type')
    lab_person = models.ForeignKey(
        LabPerson, on_delete=models.CASCADE, related_name='experiments_of_person')
    aparat = models.ForeignKey(
        Aparat, on_delete=models.CASCADE, related_name='experiments_on_this_aparat')
    progress = models.CharField(
        max_length=10,
        choices=PROGRESS_CHOICES,
        default="TBD"
    )
    final = models.BooleanField(default=False)
    # slug = models.SlugField(max_length=250)

    def get_absolute_url(self):
        return reverse(
            'experiments:editExperiment'
        )

    def __str__(self):
        return "_".join([
            self.compound.compound_name,
            self.experiment_type.experiment_name,
            str(self.id)
            ])


class Result(models.Model):
    comments = models.TextField(default="-")
    compound = models.ForeignKey(
        Compound, on_delete=models.CASCADE, related_name='results_for_compounds')
    experiment_type = models.ForeignKey(
        ExperimentType, on_delete=models.CASCADE, related_name='results_of_experiment_type')
    experiment = models.ForeignKey(
        Experiment, on_delete=models.CASCADE, related_name='results_of_experiment')
    result1 = models.FloatField(default=None, blank=True, null=True)
    result2 = models.FloatField(default=None, blank=True, null=True)
    result3 = models.FloatField(default=None, blank=True, null=True)
    result4 = models.FloatField(default=None, blank=True, null=True)
    result5 = models.FloatField(default=None, blank=True, null=True)
    # slug = models.SlugField(max_length=250)

    def get_absolute_url(self):
        return reverse(
            'experiments:editResult'
        )

    def __str__(self):
        return "_".join([
            self.compound.compound_name,
            self.experiment_type.experiment_name,
            str(self.experiment.id)
            ])
