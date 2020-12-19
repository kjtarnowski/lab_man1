from rest_framework import viewsets

from experiments.permissions import IsStaffOrReadOnly
from experiments.models import Compound, Experiment, Project, Aparat, ExperimentType, ExperimentalSet, LabPerson
from experiments.serializers import (
    CompoundSerializer,
    ExperimentSerializer,
    ProjectSerializer,
    AparatSerializer,
    ExperimentTypeSerializer,
    ExperimentalSetSerializer,
    LabPersonSerializer,
)


class LabPersonViewset(viewsets.ModelViewSet):
    queryset = LabPerson.objects.all()
    serializer_class = LabPersonSerializer
    permission_classes = [IsStaffOrReadOnly]


class CompoundViewset(viewsets.ModelViewSet):
    queryset = Compound.objects.all()
    serializer_class = CompoundSerializer
    permission_classes = [IsStaffOrReadOnly]


class ExperimentViewset(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsStaffOrReadOnly]


class AparatViewset(viewsets.ModelViewSet):
    queryset = Aparat.objects.all()
    serializer_class = AparatSerializer
    permission_classes = [IsStaffOrReadOnly]


class ExperimentTypeViewset(viewsets.ModelViewSet):
    queryset = ExperimentType.objects.all()
    serializer_class = ExperimentTypeSerializer
    permission_classes = [IsStaffOrReadOnly]


class ExperimentalSetViewset(viewsets.ModelViewSet):
    queryset = ExperimentalSet.objects.all()
    serializer_class = ExperimentalSetSerializer
