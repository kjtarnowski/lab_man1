from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from experiments.models import Project


class MLPredictApiViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(name="test_project")
        cls.user = get_user_model().objects.create_user(username="test", password="12test12", email="test@example.com")
        cls.user.save()

    def test_predict_view(self):
        input_data = {
            "Sp": "28.444",
            "nBM": "22",
            "ARR": "0.88",
            "nPyrimidines": "0",
            "HyWi_B(m)": "4.391",
            "GATS2i": "0.953",
            "Eta_betaP_A": "0.909",
            "nRNR2": "0",
            "F01[C - N]": "0",
            "MLOGP": "6.1",
        }
        classifier_url = "/api/v1/predict/random_forest/0.0.1"
        self.client.login(username="test", password="12test12")
        response = self.client.post(classifier_url, input_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["label"], "Active")
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)
