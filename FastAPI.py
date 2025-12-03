from fastapi import FastAPI
from typing import Union, Literal
from pydantic import BaseModel
import joblib
import pandas as pd

app= FastAPI()

class Features(BaseModel):
    total_area_sqm: float #
    cadastral_income: float #
    primary_energy_consumption_sqm:float #
    nbr_bedrooms: int #
    nbr_frontages: int # max 4
    subproperty_type: Literal[
        "APARTMENT", "HOUSE", "DUPLEX", "VILLA", "EXCEPTIONAL_PROPERTY",
        "FLAT_STUDIO", "GROUND_FLOOR", "PENTHOUSE", "FARMHOUSE",
        "APARTMENT_BLOCK", "COUNTRY_COTTAGE", "TOWN_HOUSE", "SERVICE_FLAT",
        "MANSION", "MIXED_USE_BUILDING", "MANOR_HOUSE", "LOFT",
        "BUNGALOW", "KOT", "CASTLE", "CHALET", "TRIPLEX", "OTHER_PROPERTY"
    ]
    province: Literal[
        "Antwerp", "East Flanders", "Brussels", "Walloon Brabant",
        "Flemish Brabant", "Liège", "West Flanders", "Hainaut",
        "Luxembourg", "Limburg", "Namur"
    ]
    fl_terrace: bool #
    fl_garden: bool #
    fl_swimming_pool: bool #
    fl_furnished: bool #
    epc: Literal["excellent","good","poor","bad","unknown"]
    
    equipped_kitchen: Literal[
        "UNKNOWN", "INSTALLED", "SEMI-EQUIPPED", "HYPER-EQUIPPED"
    ]

    heating_type: Literal[
        "GAS", "ELECTRIC", "HEAT_PUMP", "OIL", "OTHER"
    ]

model_path = "model.pkl"
pipeline = joblib.load(model_path)

@app.post("/predict")
def predict(data:Features): # Its job: Convert a web request->into model input-> into a prediction->into a web response
    df = pd.DataFrame([data.model_dump()])
    prediction = pipeline.predict(df)
    return{"predicted_price":float(prediction[0])} # Making sure it returns a dictionary

"""
There was an error caused because the model is expecting 25 features and here only 14 were passed.
The error occurs because the pipeline was trained with a ColumnTransformer that expands the 14 raw features into 25 columns internally (due to one-hot encoding and missing-value flags),
but passing a plain Python list bypasses the column names, so the transformer cannot match columns, thus shape mismatch.
By converting the Pydantic input into a df with the correct column names, the pipeline can perform all preprocessing exactly as it did during training.
This ensures the model receives the expected 25-feature array, resolving the ValueError while keeping the API clean and compatible with the trained pipeline.
"""

