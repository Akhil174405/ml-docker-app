from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator
from typing import Annotated
import numpy as np
import joblib
import redis
import os
import json

app = FastAPI()

USE_REDIS = True  # Set False to disable Redis locally

if USE_REDIS:
    import redis
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    redis_db = int(os.getenv('REDIS_DB', 0))
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
else:
    redis_client = None

model = joblib.load('iris_model.pkl')
target_names = ['setosa', 'versicolor', 'virginica']

templates = Jinja2Templates(directory="templates")


class Features(BaseModel):
    features: list[float]

    @validator('features')
    def validate_features_length(cls, v):
        if len(v) != 4:
            raise ValueError('features must be a list of exactly 4 floats')
        return v

def predict_species(features):
    prediction = model.predict([np.array(features)])
    probabilities = model.predict_proba([np.array(features)])
    confidence = float(np.max(probabilities))
    result = {
        'prediction': target_names[int(prediction[0])],
        'confidence': round(confidence, 4),
        'all_probabilities': {
            target_names[i]: round(prob, 4)
            for i, prob in enumerate(probabilities[0])
        },
        'features': features
    }
    if redis_client:
        redis_client.lpush("predictions", json.dumps(result))

    return result


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict-form")
async def predict_form(
    feature1: float = Form(...),
    feature2: float = Form(...),
    feature3: float = Form(...),
    feature4: float = Form(...)
):
    try:
        features = [feature1, feature2, feature3, feature4]
        result = predict_species(features)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@app.post("/predict")
async def predict_api(features: Features):
    try:
        result = predict_species(features.features)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def history():
    if not redis_client:
        # Redis is not enabled or not available
        return {"prediction_history": [], "error": "Prediction history is not available (Redis is disabled)."}
    raw_predictions = redis_client.lrange("predictions", 0, -1)
    parsed = [json.loads(entry) for entry in raw_predictions]
    return {"prediction_history": parsed}
