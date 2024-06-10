from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from joblib import load
import pandas as pd

model = load('model.joblib')

app = FastAPI(
    title="Prédiction de survie sur le Titanic",
    description="<b>Application de prédiction de survie sur le Titanic</b> 🚢 <br>Une version par API pour faciliter la réutilisation du modèle 🚀" +\
                "<br><br><img src=\"https://media.vogue.fr/photos/5faac06d39c5194ff9752ec9/1:1/w_2404,h_2404,c_limit/076_CHL_126884.jpg\" width=\"200\">"
)

@app.get("/", response_class=HTMLResponse, tags=["Welcome"])
async def show_welcome_page():
    """
    Show welcome page with model name and version.
    
    """
    html_content = """
    <html>
        <head>
            <title>Prédiction de survie sur le Titanic</title>
        </head>
        <body>
            <h1>Application de prédiction de survie sur le Titanic 🚢</h1>
            <form action="/submit_form" method="get">
                <label for="sex">Sex:</label>
                <input type="text" id="sex" name="sex" value="female"><br><br>
                <label for="age">Age:</label>
                <input type="number" id="age" name="age" value="29"><br><br>
                <label for="fare">Fare:</label>
                <input type="number" id="fare" name="fare" step="0.01" value="16.5"><br><br>
                <label for="embarked">Embarked:</label>
                <input type="text" id="embarked" name="embarked" value="S"><br><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/submit_form", tags=["Form"])
async def submit_form(sex: str, age: float, fare: float, embarked: str):
    """
    Handle form submission and redirect to /predict.
    """
    url = f"/predict?sex={sex}&age={age}&fare={fare}&embarked={embarked}"
    return RedirectResponse(url=url)

@app.get("/predict", tags=["Predict"])
async def predict(
    sex: str = "female",
    age: float = 29.0,
    fare: float = 16.5,
    embarked: str = "S"
) -> str:
    """
    Predict survival on the Titanic.
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
