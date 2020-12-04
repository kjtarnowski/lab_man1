from django.test import TestCase
from ml.activity_classifier.random_forest_activity_classifier import RandomForestClassifier


class MLTests(TestCase):
    def test_rf_algorithm(self):
        input_data = {
            "Sp": 28.444,
            "nBM": 22,
            "ARR": 0.88,
            "nPyrimidines": 0,
            "HyWi_B(m)": 4.391,
            "GATS2i": 0.953,
            "Eta_betaP_A": 0.909,
            "nRNR2": 0,
            "F01[C - N]": 0,
            "MLOGP": 6.1
        }

        my_alg = RandomForestClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual('Active', response['label'])
