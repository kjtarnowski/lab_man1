import json
from rest_framework import viewsets, views, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from ml.models import MLAlgorithm, MLRequest
from ml.serializers import MLAlgorithmSerializer, MLRequestSerializer
from ml.activity_classifier.activity_classifier_with_basic_imputer import ActivityClassifier


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsStaffOrReadOnly(BasePermission):
    """
    The request is authenticated as staff user, or is a read-only request form authenticated user.
    """

    def has_permission(self, request, view):
        if request.user.is_staff or request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        return False


class MLAlgorithmViewset(viewsets.ModelViewSet):
    queryset = MLAlgorithm.objects.all()
    serializer_class = MLAlgorithmSerializer
    permission_classes = [IsStaffOrReadOnly]


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

        algorithm_object = ActivityClassifier(encoders=algorithm.joblib_binary_file_encoders,
                                              model=algorithm.joblib_binary_file_algorithm)
        prediction = algorithm_object.compute_prediction_for_one_sample(request.data)


        label = prediction["label"] if "label" in prediction else "error"
        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            mlalgorithm=algorithm,
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id

        return Response(prediction)
