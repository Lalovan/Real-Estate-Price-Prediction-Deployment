# Real-estate-price-prediction-Regression
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-337ab7?logo=xgboost&logoColor=white)


### ⏩ At a Glance: ###

This is an end-to-end machine learning project that predicts Belgian real estate prices using a trained XGBoost model, served through a FastAPI backend and deployed with a public Streamlit web application.  

***Live App:***
https://real-estate-price-prediction-immo-eliza.streamlit.app/ 

# 🚀 Project mission #

This repository documents the final deployment stage of Immo Eliza’s broader data pipeline, whose mission is to deliver faster and more accurate property price estimations across Belgium. 

The previous stages include initial data scraping and exploratory data analysis (EDA), preprocessing, model development, and evaluation.

# 📌 Project Context #
Immo Eliza (imaginary real estate firm) aims to strengthen decision-making and valuation precision by integrating data-driven modeling. After gathering Belgian real estate data (web scraping), conducting early analysis (EDA), building a robust predictive model (XGBoost), the next step is to wrap up the functioning ML product in an application.

This repository provides:
- model serialization (joblib/pickle);
- API exposure and deployment to cloud (Render);
- Interactive web app integration via Streamli;


# 🧭 Workflow Overview #
### 1. Model Serialization  
- Best model (XGBoost) saved using `joblib` / `pickle`
- Reusable for batch or real-time inference  

### 2. API Development & Deployment  
- Model exposed via **FastAPI**
- Hosted on **Render** for public access  

### 3. Web Application
- Frontend UI for user inputs (**Streamlit**) 
- Sends requests to the deployed API  
- Displays real-time predicted property price  


# 🌳 Repository Structure #

```
Real-estate-price-prediction-Regression
│
├── app.py           # Streamlit web application (frontend)
├── FastAPI.py       # API exposing the trained model (backend)
├── model.pkl        # Serialized trained XGBoost model
├── requirements.txt # Dependencies
├── .gitignore       # Ignore rules
├── README.md        # Project documentation

```



# ⚙️ Installation and Execution #

**1. Clone the repository:**

`git clone https://github.com/Lalovan/Real-Estate-Price-Prediction-Deployment.git`

`cd Real-Estate-Price-Prediction-Deployment`

**2. Create and activate a virtual environment (optional):**

`python -m venv venv`

`source venv/bin/activate      # macOS/Linux`

`venv\Scripts\activate         # Windows`


**3. Install dependencies:**

`pip install -r requirements.txt`

**4. Run local price predictions**

`python app.py`

**5. Use the deployed application**

***Streamlit App***: https://real-estate-price-prediction-immo-eliza.streamlit.app/  


# ⏰ Timeline #

4 working days

# 🔮 Next Steps #

🎨 The next goal of this project is to make the application **more visually appealing and user-friendly**, turning it from a functional ML tool into a more polished product.