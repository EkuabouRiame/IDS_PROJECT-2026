import joblib
import pandas as pd

# Load trained model
model = joblib.load("models/random_forest.pkl")

def predict_data(data):
    prediction = model.predict(data)
    return prediction