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


