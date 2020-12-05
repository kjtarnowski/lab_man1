from enum import Enum

import joblib
import pandas as pd

from django.conf import settings


class Label(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class StatusChoice(Enum):
    OK = "OK"
    ERROR = "Error"


class RandomForestClassifier:
    def __init__(self):
        self.encoders = joblib.load(settings.ENCODERS_PATH)
        self.model = joblib.load(settings.MODEL_PATH)

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])
        input_data_transformed = self.encoders.transform(input_data)
        return input_data_transformed

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        label = Label.INACTIVE.value
        if input_data[1] > 0.5:
            label = Label.ACTIVE.value
        return {"probability": input_data[1], "label": label, "status": StatusChoice.OK.value}

    def compute_prediction(self, input_data):  # compute prediction for one sample
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]  # one sample
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": StatusChoice.ERROR.value, "message": str(e)}
        return prediction
