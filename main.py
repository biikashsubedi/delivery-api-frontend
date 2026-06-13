from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import joblib
import pandas as pd

# API and Security Configuration
app = FastAPI(title="Delivery Time Prediction API")
API_KEY = "seneca-aigc-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key")

# Model Loading
model = joblib.load('delivery_model.joblib')

# Data Structure Definition
class DeliveryRequest(BaseModel):
    Delivery_person_Age: float
    Delivery_person_Ratings: float
    Vehicle_condition: int
    multiple_deliveries: float
    Distance_km: float
    Weather: str
    Road_traffic_density: str
    Type_of_order: str
    Type_of_vehicle: str
    Festival: str
    City: str

# Authentication Logic
def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# Prediction Endpoint
@app.post("/predict")
def predict_delivery_time(request: DeliveryRequest, api_key: str = Security(get_api_key)):
    input_data = pd.DataFrame([request.model_dump()])
    prediction = model.predict(input_data)
    return {"estimated_time_minutes": round(prediction[0], 2)}