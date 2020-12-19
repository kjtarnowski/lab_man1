from ml.models import MLAlgorithm


class MLRegistry:
    def __init__(self):
        self.algorithms = {}

    def add_algorithm(self, algorithm_object, algorithm_name, algorithm_version, algorithm_description):
        MLAlgorithm.objects.get_or_create(
            name=algorithm_name, description=algorithm_description, version=algorithm_version
        )

        self.algorithms[algorithm_name] = algorithm_object
