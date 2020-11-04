# import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.urls import reverse
from django.contrib.postgres.fields import JSONField

from .managers import LabPersonManager


class LabPerson(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, unique=True)
    lab_email = models.EmailField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['lab_email']
    objects = LabPersonManager()


class Project(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Aparat(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class ExperimentalSet(models.Model):
    name = models.CharField(max_length=25)
    experiment_date = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Compound(models.Model):
    name = models.CharField(max_length=25, unique=True)
    mass = models.FloatField(blank=True, null=True, default=None)
    monoisotopic_mass = models.FloatField(blank=True, null=True, default=None)
    formula = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default=None)
    comments = models.TextField(default="-")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='compounds_of_the_project'
        )

    def __str__(self):
        return self.name


class Experiment(models.Model):
    PROGRESS_CHOICES = (
        ("TBD", "TBD"),
        ("ONGOING", "ONGOING"),
        ("UC", "UC"),
        ("TO_REP", "TO_REP")
    )
    comments = models.TextField(default="-")
    experiment_date = models.DateField(default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    compound = models.ForeignKey(
        Compound,
        on_delete=models.CASCADE,
        related_name='experiments_for_compound')
    lab_person = models.ForeignKey(
        LabPerson,
        on_delete=models.CASCADE,
        related_name='experiments_of_person'
        )
    aparat = models.ForeignKey(
        Aparat,
        on_delete=models.CASCADE,
        related_name='experiments_on_this_aparat')
    experimental_set = models.ForeignKey(
        ExperimentalSet,
        on_delete=models.CASCADE,
        related_name='experiments_of_this_set',
        blank=True, null=True, default=None
        )
    progress = models.CharField(
        max_length=10,
        choices=PROGRESS_CHOICES,
        default="TBD"
    )
    final = models.BooleanField(default=False)
    experimental_results = JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['compound', 'experimental_set'],
                name='compoud_from_set')
        ]

    def get_absolute_url(self):
        return reverse(
            'experiments:editExperiment'
        )

    def __str__(self):
        return "_".join([
            self.experimental_set.name,
            self.compound.name,
            str(self.id)
            ])


class Experiment_Sp(Experiment):
    result_Sp = models.FloatField(default=None, blank=True, null=True)
    result_HyWi = models.FloatField(default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.final:
            try:
                res_obj = Result.objects.get(compound=self.compound)
                setattr(res_obj, 'experiment_Sp', self)
                res_obj.save()
            except Result.DoesNotExist:
                res_obj = Result.objects.create(
                    compound=self.compound,
                    experiment_Sp=self,
                    )
        super().save(*args, **kwargs)


class Experiment_ARR(Experiment):
    result_ARR = models.FloatField(default=None, blank=True, null=True)
    result_GSTS2i = models.FloatField(default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.final:
            try:
                res_obj = Result.objects.get(compound=self.compound)
                setattr(res_obj, 'experiment_ARR', self)
                res_obj.save()
            except Result.DoesNotExist:
                res_obj = Result.objects.create(
                    compound=self.compound,
                    experiment_ARR=self,
                    )
        super().save(*args, **kwargs)


class Experiment_MLOGP(Experiment):
    result_MLOGP = models.FloatField(default=None, blank=True, null=True)
    result_Eta_beta = models.FloatField(default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.final:
            try:
                res_obj = Result.objects.get(compound=self.compound)
                setattr(res_obj, 'experiment_MLOGP', self)
                res_obj.save()
            except Result.DoesNotExist:
                res_obj = Result.objects.create(
                    compound=self.compound,
                    experiment_MLOGP=self,
                    )
        super().save(*args, **kwargs)


class Result(models.Model):
    compound = models.ForeignKey(
        Compound,
        on_delete=models.CASCADE,
        related_name='results_for_compounds',
        default=None,
        blank=True,
        null=True,
        unique=True
        )
    experiment_Sp = models.ForeignKey(
        Experiment_Sp,
        on_delete=models.SET_NULL,
        related_name='results_of_experiment_Sp',
        default=None,
        blank=True,
        null=True
        )
    experiment_ARR = models.ForeignKey(
        Experiment_ARR,
        on_delete=models.SET_NULL,
        related_name='results_of_experiment_ARR',
        default=None,
        blank=True,
        null=True
        )
    experiment_MLOGP = models.ForeignKey(
        Experiment_MLOGP,
        on_delete=models.SET_NULL,
        related_name='results_of_experiment_MLOGP',
        default=None,
        blank=True,
        null=True
        )
    comments = models.TextField(default="-")

    def get_absolute_url(self):
        return reverse(
            'experiments:editResult'
        )

    def __str__(self):
        return "_".join([
            self.compound.name,
            "result_id",
            str(self.id)
            ])
