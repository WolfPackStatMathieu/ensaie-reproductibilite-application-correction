"""A simple API to expose our trained RandomForest model for Tutanic survival."""
from fastapi import FastAPI
from joblib import load

import pandas as pd
import os


# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
model = load(model_path)

app = FastAPI(
    title="Prédiction de survie sur le Titanic",
    description=
    "<b>Application de prédiction de survie sur le Titanic</b> 🚢 <br>Une version par API pour faciliter la réutilisation du modèle 🚀" +\
        "<br><br><img src=\"https://media.vogue.fr/photos/5faac06d39c5194ff9752ec9/1:1/w_2404,h_2404,c_limit/076_CHL_126884.jpg\" width=\"200\">"
    ,root_path="/proxy/5000/")


@app.get("/", tags=["Welcome"])
def show_welcome_page():
    """
    Show welcome page with model name and version.
    """

    return {
        "Message": "API de prédiction de survie sur le Titanic",
        "Model_name": 'Titanic ML',
        "Model_version": "0.1",
    }


@app.get("/predict", tags=["Predict"])
async def predict(
    sex: str = "female",
    age: float = 29.0,
    fare: float = 16.5,
    embarked: str = "S"
) -> str:
    """
    """

    df = pd.DataFrame(
        {
            "Sex": [sex],
            "Age": [age],
            "Fare": [fare],
            "Embarked": [embarked],
        }
    )

    prediction = "Survived 🎉" if int(model.predict(df)) == 1 else "Dead ⚰️"

    return prediction

    @app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}

