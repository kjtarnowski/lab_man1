from rest_framework import routers

from experiments.api_views import ExperimentViewset, CompoundViewset, ExperimentTypeViewset, AparatViewset, \
    ProjectViewset, LabPersonViewset, ExperimentalSetViewset
from ml.api_views import MLAlgorithmViewset, MLRequestViewset

router = routers.DefaultRouter()
router.register(r"compounds", CompoundViewset)
router.register(r"experiments", ExperimentViewset)
router.register(r"experimenttypes", ExperimentTypeViewset)
router.register(r"aparats", AparatViewset)
router.register(r"projects", ProjectViewset)
router.register(r"labpersons", LabPersonViewset)
router.register(r"experimentalsets", ExperimentalSetViewset)
router.register(r"mlalgorithms", MLAlgorithmViewset)
router.register(r"mlrequests", MLRequestViewset)
