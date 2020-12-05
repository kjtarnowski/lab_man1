from io import BytesIO
from enum import Enum
import joblib
import pandas as pd


class Label(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class StatusChoice(Enum):
    OK = "OK"
    ERROR = "Error"


class ActivityClassifier:
    def __init__(self, encoders, model):
        model_file = BytesIO(encoders.tobytes())
        encoder_file = BytesIO(model.tobytes())
        self.encoders = joblib.load(model_file)
        self.model = joblib.load(encoder_file)

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

    def compute_prediction_for_one_sample(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": StatusChoice.ERROR.value, "message": str(e)}
        return prediction
