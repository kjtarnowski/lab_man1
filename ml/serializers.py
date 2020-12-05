from rest_framework import serializers
from . import models


class MLAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MLAlgorithm
        fields = "__all__"


class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MLRequest
        fields = "__all__"
