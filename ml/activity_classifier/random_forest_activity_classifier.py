import joblib
import pandas as pd


class RandomForestClassifier:
    def __init__(self):
        path_to_artifacts = "ml/activity_classifier/"
        self.encoders = joblib.load(path_to_artifacts + "median_imputer.joblib")
        self.model = joblib.load(path_to_artifacts + "CV_random_forest_classifier_best_estimator.joblib")

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])
        input_data_transformed = self.encoders.transform(input_data)
        return input_data_transformed

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        label = "Inactive"
        if input_data[1] > 0.5:
            label = "Active"
        return {"probability": input_data[1], "label": label, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]  #one sample
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        return prediction
