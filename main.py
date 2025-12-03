from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

app= FastAPI()

class Features(BaseModel):
    
    total_area_sqm: int
    cadastral_income: int
    primary_energy_consumption_sqm:int
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

@app.post("/predict")
def predict(data:Features):
    test_data=[[data.total_area_sqm,
    data.cadastral_income,
    data.primary_energy_consumption_sqm,
    data.nbr_bedrooms,
    data.nbr_frontages,
    data.subproperty_type,
    data.province,
    data.fl_terrace,
    data.fl_garden,
    data.fl_swimming_pool,
    data.fl_furnished,
    data.epc,
    data.equipped_kitchen,
    data.heating_type
    ]]




