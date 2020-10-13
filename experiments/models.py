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

    def __str__(self):
        return self.project_name


class Aparat(models.Model):
    aparat_name = models.CharField(max_length=25)

    def __str__(self):
        return self.aparat_name


# class ExperimentType(models.Model):
#     experiment_name = models.CharField(max_length=25)

#     def __str__(self):
#         return self.experiment_name


class ExperimentalSet(models.Model):
    set_name = models.CharField(max_length=25)
    experiment_date = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.set_name


class Compound(models.Model):
    compound_name = models.CharField(max_length=25,unique=True,primary_key=True)
    compound_mass = models.FloatField(blank=True, null=True, default=None)
    compound_monoisotopic_mass = models.FloatField(blank=True, null=True, default=None)
    compound_formula = models.CharField(max_length=50, blank=True, null=True, default=None)
    comments = models.TextField(default="-")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='compounds_of_the_project')

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
        Compound, on_delete=models.CASCADE, related_name='experiments_for_compound')
    # experiment_type = models.ForeignKey(
    #     ExperimentType, on_delete=models.CASCADE, related_name='experiments_of_this_type')
    lab_person = models.ForeignKey(
        LabPerson, on_delete=models.CASCADE, related_name='experiments_of_person')
    aparat = models.ForeignKey(
        Aparat, on_delete=models.CASCADE, related_name='experiments_on_this_aparat')
    experimental_set = models.ForeignKey(
        ExperimentalSet, on_delete=models.CASCADE, related_name='experiments_of_this_set', blank=True,
    null=True, default=None)
    progress = models.CharField(
        max_length=10,
        choices=PROGRESS_CHOICES,
        default="TBD"
    )
    final = models.BooleanField(default=False)
    # slug = models.SlugField(max_length=250)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['compound', 'experimental_set'], name='compoud_from_set')
        ]

    def get_absolute_url(self):
        return reverse(
            'experiments:editExperiment'
        )

    def __str__(self):
        return "_".join([
            self.experimental_set.set_name,
            self.compound.compound_name,
            str(self.id)
            ])


class Experiment_Sp(Experiment):
    result_Sp = models.FloatField(default=None, blank=True, null=True)
    result_HyWi = models.FloatField(default=None, blank=True, null=True)


class Experiment_ARR(Experiment):
    result_ARR = models.FloatField(default=None, blank=True, null=True)
    result_GSTS2i = models.FloatField(default=None, blank=True, null=True)


class Experiment_MLOGP(Experiment):
    result_MLOGP = models.FloatField(default=None, blank=True, null=True)
    result_Eta_beta = models.FloatField(default=None, blank=True, null=True)


class Result(models.Model):
    compound = models.ForeignKey(
        Compound, on_delete=models.CASCADE, related_name='results_for_compounds',default=None, blank=True, null=True)
    experiment_Sp = models.ForeignKey(
        Experiment_Sp, on_delete=models.CASCADE, related_name='results_of_experiment',default=None, blank=True, null=True)
    experiment_ARR = models.ForeignKey(
        Experiment_ARR, on_delete=models.CASCADE, related_name='results_of_experiment',default=None, blank=True, null=True)
    experiment_MLOGP = models.ForeignKey(
        Experiment_MLOGP, on_delete=models.CASCADE, related_name='results_of_experiment',default=None, blank=True, null=True)
    result_Sp = models.FloatField(default=None, blank=True, null=True)
    result_HyWi = models.FloatField(default=None, blank=True, null=True)
    result_ARR = models.FloatField(default=None, blank=True, null=True)
    result_GSTS2i = models.FloatField(default=None, blank=True, null=True)
    result_MLOGP = models.FloatField(default=None, blank=True, null=True)
    result_Eta_beta = models.FloatField(default=None, blank=True, null=True)
    comments = models.TextField(default="-")

    def get_absolute_url(self):
        return reverse(
            'experiments:editResult'
        )

    def __str__(self):
        return "_".join([
            self.compound.compound_name,
            "result_id",
            str(self.id)
            ])
