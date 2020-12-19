from rest_framework import routers

from experiments.api_views import ExperimentViewset, CompoundViewset

router = routers.DefaultRouter()
router.register(r"compounds", CompoundViewset)
router.register(r"experiments", ExperimentViewset)
