"""
WSGI config for lab_man1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from ml.activity_classifier.random_forest_activity_classifier import RandomForestClassifier
from ml.registry import MLRegistry

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab_man1.settings")

application = get_wsgi_application()


try:
    registry = MLRegistry()
    rf = RandomForestClassifier()

    registry.add_algorithm(algorithm_object=rf,
                            algorithm_name="random_forest",
                            algorithm_version="0.0.1",
                            algorithm_description="Random Forest with median imputer preprocessing")

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
