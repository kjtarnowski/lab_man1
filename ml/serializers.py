from rest_framework import serializers

from ml.models import MLAlgorithm, MLRequest


class MLAlgorithmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithm
        fields = "__all__"


class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        fields = "__all__"
