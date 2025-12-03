import streamlit as st
import pandas as pd
import joblib
import requests # Relevant for the API

# ------------------------------
# Loading model
# ------------------------------
@st.cache_resource #Decorator that adds to the behaviour of def below (let's the model load only once)
def load_model():
    return joblib.load("model.pkl")

pipeline = load_model()

# ------------------------------
# Initialization of session state/Wizard
# ------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1


# ------------------------------
# UI Title
# ------------------------------
st.title(" ") # Not necessary for the moment

# ------------------------------
# Initializing defaults for a set of features
# ------------------------------

defaults = {
    "step": 1,
    "total_area_sqm": 100,
    "cadastral_income": 0,
    "primary_energy_consumption_sqm": 100,
    "nbr_bedrooms": 2,
    "nbr_frontages": 2,
    "subproperty_type": "APARTMENT",
    "province": "Antwerp",
    "fl_terrace": False,
    "fl_garden": False,
    "fl_swimming_pool": False,
    "fl_furnished": False,
    "epc": "good",
    "equipped_kitchen": "UNKNOWN",
    "heating_type": "GAS"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ------------------------------
# STEP 0 — LANDING PAGE
# ------------------------------
if st.session_state.step == 0:

    st.markdown(
        """
        <div style="
            text-align: center; 
            padding: 60px 20px;
        ">
            <h1 style="margin-bottom: 20px;">Immo Eliza Price Prediction</h1>
            <p style="font-size: 18px; line-height: 1.6;">
                Welcome to the Immo Eliza Price Prediction tool!
            </p>
            <p style="font-size: 18px; line-height: 1.6;">
                This tool helps you estimate an accurate property price  
                based on real Belgian real estate market data. 
            </p>
            <p style="font-size: 18px; line-height: 1.6;"> 
                Whether you're planning to <strong>sell</strong> or <strong>buy</strong>,  
                our model gives you a data-driven estimate in seconds.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Centering the button
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.button(
            "🔍 Predict Price",
            key="start_button",
            on_click=lambda: st.session_state.update({"step": 1}),
            use_container_width=True
        )

    st.stop()  # prevent the rest of the script from running

# ------------------------------
# STEP 1 — PROPERTY BASICS
# ------------------------------
if st.session_state.step == 1:
    st.header("Step 1 of 4 — Property Basics")

    subtype_labels = {'Apartment':'APARTMENT','House': 'HOUSE','Duplex':'DUPLEX','Villa': 'VILLA', 'Exceptional property':'EXCEPTIONAL_PROPERTY', 'Flat studio':'FLAT_STUDIO', 'Ground floor':'GROUND_FLOOR', 
         'Penthouse':'PENTHOUSE', 'Farmhouse':'FARMHOUSE', 'Apartment block':'APARTMENT_BLOCK', 'Country cottage':'COUNTRY_COTTAGE', 'Town house':'TOWN_HOUSE', 'Service flat':'SERVICE_FLAT', 
         'Mansion':'MANSION', 'Mixed use building':'MIXED_USE_BUILDING', 'Manor house':'MANOR_HOUSE', 'Loft':'LOFT', 'Bungalow':'BUNGALOW','Kot': 'KOT', 'Castle': 'CASTLE', 'Chalet':'CHALET',
         'Triplex':'TRIPLEX', 'Other property':'OTHER_PROPERTY'}
    
    #Transition/helper variable
    clean_subtypes = list(subtype_labels.keys())

    #This one saves the "beautiful choice"
    selected_subproperty= st.selectbox(
        "Property sub-type",
        options=clean_subtypes
    )

    st.session_state.subproperty_type = subtype_labels[selected_subproperty] #This one passes the "ugly" choice to the preprocessor

    st.session_state.province = st.selectbox(
        "Province",
        ['Antwerp', 'East Flanders', 'Brussels', 'Walloon Brabant', 'Flemish Brabant', 
          'Liège', 'West Flanders', 'Hainaut', 'Luxembourg', 'Limburg', 'Namur'],
        index=0 if "province" not in st.session_state else
        ['Antwerp', 'East Flanders', 'Brussels', 'Walloon Brabant', 'Flemish Brabant', 
          'Liège', 'West Flanders', 'Hainaut', 'Luxembourg', 'Limburg', 'Namur'].index(st.session_state.province)
    )

    st.session_state.total_area_sqm = st.number_input(
        "Total area (m²)",
        min_value=10,
        max_value=2000,
        step=1,
        value=st.session_state.get("total_area_sqm", 100) # To eventually replace with median 
    )

    st.session_state.nbr_bedrooms = st.number_input(
        "Number of bedrooms",
        min_value=0,
        max_value=20,
        value=st.session_state.get("nbr_bedrooms", 2)
    )

    st.session_state.nbr_frontages = st.number_input(
        "Number of frontages",
        min_value=1,
        max_value=4,
        value=st.session_state.get("nbr_frontages", 2)
    )

    st.session_state.cadastral_income = st.number_input(
        "Cadastral Income",
        min_value=0,
        max_value=10000,
        step=100,
        value=st.session_state.get("cadastral_income", 0),
        help = "Tax-based estimate of property’s rental value used by Belgium authorities."
    )

    col1, col2 = st.columns([4, 1])
    with col2:
        st.button("Next ", on_click=next_step)

# ------------------------------
# STEP 2 — ENERGY & INSTALLATIONS
# ------------------------------

elif st.session_state.step == 2:
    st.header("Step 2 of 4 — Energy & Installations")

    st.session_state.epc = st.selectbox(
        "Energy Performance Certificate (EPC) Rating",
        ["excellent", "good", "poor", "bad", "unknown"],
        index=1 if "epc" not in st.session_state else
        ["excellent", "good", "poor", "bad","unknown"].index(st.session_state.epc),
        help="EPC categories:\n"
    "- excellent: A+,A (Flanders), A(Brussels), A++, A+ (Wallonia)\n"
    "- good: B (Flanders), B,C (Brussels), A,B (Wallonia)\n"
    "- poor: C,D (Flanders), D,E (Brussels) , C,D,E (Wallonia)\n"
    "- bad: E,F (Fanders), F,G (Brussels), F,G (Wallonia)"
    )
    
    st.session_state.primary_energy_consumption_sqm = st.number_input(
        "Primary energy consumption (kWh/m²)",
        min_value=0,
        max_value=2000,
        value=st.session_state.get("primary_energy_consumption_sqm", 100)
    )

    st.session_state.heating_type = st.selectbox(
        "Heating type",
        ["GAS", "ELECTRIC", "HEAT PUMP", "OIL", "OTHER"],
        index=0 if "heating_type" not in st.session_state else
        ["GAS", "ELECTRIC", "HEAT PUMP", "OIL", "OTHER"].index(st.session_state.heating_type)
    )

    st.session_state.equipped_kitchen = st.selectbox(
        "Kitchen equipment",
        ["UNKNOWN", "INSTALLED", "SEMI-EQUIPPED", "HYPER-EQUIPPED"],
        index=0 if "equipped_kitchen" not in st.session_state else
        ["UNKNOWN", "INSTALLED", "SEMI-EQUIPPED", "HYPER-EQUIPPED"].index(st.session_state.equipped_kitchen)
    )

    col1, col2 = st.columns([4,1])
    with col1:
        st.button("Back", on_click=prev_step)
    with col2:
        st.button("Next", on_click=next_step)



# ------------------------------
# STEP 3 — AMENITIES
# ------------------------------
elif st.session_state.step == 3:
    st.header("Step 3 of 4 — Amenities")

    st.session_state.fl_terrace = st.toggle(
        "Terrace", value=bool(st.session_state.get("fl_terrace", False))
    )
    st.session_state.fl_garden = st.toggle(
        "Garden", value=bool(st.session_state.get("fl_garden", False))
    )
    st.session_state.fl_swimming_pool = st.toggle(
        "Swimming pool", value=bool(st.session_state.get("fl_swimming_pool", False))
    )
    st.session_state.fl_furnished = st.toggle(
        "Furnished", value=bool(st.session_state.get("fl_furnished", False))
    )

    col1, col2 = st.columns([4,1])
    with col1:
        st.button("Back", on_click=prev_step)
    with col2:
        st.button("Next", on_click=next_step)



# ------------------------------
# STEP 4 — SUMMARY & PREDICT
# ------------------------------
elif st.session_state.step == 4:
    st.header("Step 4 of 4 — Review Data")
    st.markdown("### Please verify all inputs before predicting:")

    review_data = {
        "Total area (m²)": st.session_state.total_area_sqm,
        "Cadastral income": st.session_state.cadastral_income,
        "Primary energy consumption (m²)": st.session_state.primary_energy_consumption_sqm,
        "Bedrooms": st.session_state.nbr_bedrooms,
        "Frontages": st.session_state.nbr_frontages,
        "Property type": st.session_state.subproperty_type,
        "Province": st.session_state.province,
        "Terrace": "Yes" if st.session_state.fl_terrace else "No",
        "Garden": "Yes" if st.session_state.fl_garden else "No",
        "Swimming pool": "Yes" if st.session_state.fl_swimming_pool else "No",
        "Furnished": "Yes" if st.session_state.fl_furnished else "No",
        "EPC": st.session_state.epc,
        "Equipped kitchen": st.session_state.equipped_kitchen,
        "Heating type": st.session_state.heating_type
    }

    st.table(pd.DataFrame(review_data.items(), columns=["Specification", "Selection"]))

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", on_click=prev_step)
    with col2:
        if st.button("Predict Price", use_container_width=True):
            st.session_state.step = 5



# ------------------------------
# STEP 5 — RESULT
# ------------------------------
elif st.session_state.step == 5:
    st.header("Prediction Result")

    # Build dataframe for prediction
    df = pd.DataFrame([{
        "total_area_sqm": st.session_state.total_area_sqm,
        "cadastral_income": st.session_state.get("cadastral_income", 0),
        "primary_energy_consumption_sqm": st.session_state.primary_energy_consumption_sqm,
        "nbr_bedrooms": st.session_state.nbr_bedrooms,
        "nbr_frontages": st.session_state.nbr_frontages,
        "subproperty_type": st.session_state.subproperty_type,
        "province": st.session_state.province,
        "fl_terrace": int(st.session_state.fl_terrace),
        "fl_garden": int(st.session_state.fl_garden),
        "fl_swimming_pool": int(st.session_state.fl_swimming_pool),
        "fl_furnished": int(st.session_state.fl_furnished),
        "epc": st.session_state.epc,
        "equipped_kitchen": st.session_state.equipped_kitchen,
        "heating_type": st.session_state.heating_type
    }])

    # Correct dtype casting
    int_cols = [
        "total_area_sqm", "cadastral_income", "primary_energy_consumption_sqm",
        "nbr_bedrooms", "nbr_frontages", "fl_terrace", "fl_garden",
        "fl_swimming_pool", "fl_furnished"
    ]
    for col in int_cols:
        df[col] = df[col].astype("Int64")

    # Prediction
    #with st.spinner("Predicting price..."):
        #prediction = pipeline.predict(df)[0]

    #st.success(f"Estimated Property Price: €{prediction:,.0f}")

    #st.button("New Prediction", on_click=lambda: st.session_state.update({"step": 1}))

    # Prediction (API)

api_url= "https://real-estate-price-prediction-immoeliza.onrender.com/predict"

payload = {
"total_area_sqm": st.session_state.total_area_sqm,
"cadastral_income": st.session_state.cadastral_income,
"primary_energy_consumption_sqm": st.session_state.primary_energy_consumption_sqm,
"nbr_bedrooms": st.session_state.nbr_bedrooms,
"nbr_frontages": st.session_state.nbr_frontages,
"subproperty_type": st.session_state.subproperty_type,
"province": st.session_state.province,
"fl_terrace": st.session_state.fl_terrace,
"fl_garden": st.session_state.fl_garden,
"fl_swimming_pool": st.session_state.fl_swimming_pool,
"fl_furnished": st.session_state.fl_furnished,
"epc": st.session_state.epc,
"equipped_kitchen": st.session_state.equipped_kitchen,
"heating_type": st.session_state.heating_type
}

# Send POST request
response = requests.post(api_url, json=payload)
result = response.json()
print(result)