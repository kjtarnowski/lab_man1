import json
from rest_framework import viewsets, views, status
from rest_framework.response import Response

from experiments.models import Compound, Experiment, Project, Aparat, ExperimentType, ExperimentalSet, LabPerson
from experiments.serializers import (
    CompoundSerializer,
    ExperimentSerializer,
    ProjectSerializer,
    AparatSerializer,
    ExperimentTypeSerializer,
    ExperimentalSetSerializer,
    LabPersonSerializer
)


class LabPersonViewset(viewsets.ModelViewSet):
    queryset = LabPerson.objects.all()
    serializer_class = LabPersonSerializer


class CompoundViewset(viewsets.ModelViewSet):
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer


class ExperimentViewset(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class AparatViewset(viewsets.ModelViewSet):
    queryset = Aparat.objects.all()
    serializer_class = AparatSerializer


class ExperimentTypeViewset(viewsets.ModelViewSet):
    queryset = ExperimentType.objects.all()
    serializer_class = ExperimentTypeSerializer

