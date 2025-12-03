from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
import joblib
import pandas as pd

app= FastAPI()

class Features(BaseModel):
    total_area_sqm: float
    cadastral_income: float
    primary_energy_consumption_sqm:float
    nbr_bedrooms: int
    nbr_frontages: int
    subproperty_type:str
    province:str
    fl_terrace: bool
    fl_garden: bool
    fl_swimming_pool: bool
    fl_furnished: bool
    epc: str
    equipped_kitchen:str
    heating_type:str

model_path = "model.pkl"
pipeline = joblib.load(model_path)

@app.post("/predict")
def predict(data:Features): # Its job: Convert a web request->into model input-> into a prediction->into a web response
    df = pd.DataFrame([data.model_dump()])
    prediction = pipeline.predict(df)
    return{"The predicted price of real estate property is: ",float(prediction[0])} # Making sure it returns a dictionary

"""
There was an error caused because the model is expecting 25 features and here only 14 were passed.
The error occurs because the pipeline was trained with a ColumnTransformer that expands the 14 raw features into 25 columns internally (due to one-hot encoding and missing-value flags),
but passing a plain Python list bypasses the column names, so the transformer cannot match columns, thus shape mismatch.
By converting the Pydantic input into a df with the correct column names, the pipeline can perform all preprocessing exactly as it did during training.
This ensures the model receives the expected 25-feature array, resolving the ValueError while keeping the API clean and compatible with the trained pipeline.
"""

