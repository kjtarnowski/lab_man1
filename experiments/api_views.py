import json
from rest_framework import viewsets, views, status
from rest_framework.permissions import BasePermission

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

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsStaffOrReadOnly(BasePermission):
    """
    The request is authenticated as staff user, or is a read-only request form authenticated user.
    """

    def has_permission(self, request, view):
        if request.user.is_staff or request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        return False



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
