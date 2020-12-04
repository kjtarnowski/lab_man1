import json
from rest_framework import viewsets, views, status
from rest_framework.response import Response

from experiments.models import Compound, Experiment, Project, Aparat, ExperimentType, ExperimentalSet, LabPerson, MLAlgorithm, MLRequest
from experiments.serializers import (
    CompoundSerializer,
    ExperimentSerializer,
    ProjectSerializer,
    AparatSerializer,
    ExperimentTypeSerializer,
    ExperimentalSetSerializer,
    LabPersonSerializer,
    MLAlgorithmSerializer,
    MLRequestSerializer
)
from lab_man1.wsgi import registry


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


class MLAlgorithmViewset(viewsets.ModelViewSet):
    queryset = MLAlgorithm.objects.all()
    serializer_class = MLAlgorithmSerializer


class MLRequestViewset(viewsets.ModelViewSet):
    queryset = MLRequest.objects.all()
    serializer_class = MLRequestSerializer


class PredictView(views.APIView):
    def post(self, request, algorithm_name, algorithm_version):
        algorithm = MLAlgorithm.objects.filter(name=algorithm_name, version=algorithm_version).last()

        if algorithm is None:
            return Response(
                {"status": "Error", "message": "ML algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        algorithm_object = registry.algorithms[algorithm.name]
        prediction = algorithm_object.compute_prediction(request.data)


        label = prediction["label"] if "label" in prediction else "error"
        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            mlalgorithm=algorithm,
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id

        return Response(prediction)
