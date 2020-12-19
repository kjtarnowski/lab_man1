from rest_framework import serializers

from experiments import models


class LabPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LabPerson
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = "__all__"


class AparatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Aparat
        fields = "__all__"


class ExperimentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperimentType
        fields = "__all__"


class ExperimentalSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperimentalSet
        fields = "__all__"


class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Compound
        fields = "__all__"


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Experiment
        fields = "__all__"
