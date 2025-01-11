#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Final

BASE_PATH: Final = Path(__file__).resolve().parent
ROOT_PATH: Final = BASE_PATH

import dotenv

dotenv.load_dotenv(ROOT_PATH / "service.env", override=False)

import pickle

import flask

from models import RecommendRequest, RecommendResponse

app = flask.Flask("TP2-Backend")

with open(os.environ["MODEL_PATH"], "rb") as model_file:
    app.model = pickle.load(model_file)

app.version = os.environ["VERSION"]
app.model_date = os.environ["MODEL_DATE"]

def recommend_items (current_items, max_recommend: int = 20) -> list[str]:
    recommendations = set()

    for rule in app.model:
        antecedent, consequent, _ = rule
        if set(antecedent).issubset(current_items):
            recommendations.update(consequent)

    return list(recommendations - set(current_items))[:max_recommend]

@app.route("/api/recommend", methods=["POST"])
def recommend () -> flask.Response:
    if flask.request.content_type != "application/json":
        return flask.Response("Content-Type must be application/json", status=415)

    req = RecommendRequest(**flask.request.json)

    resp = RecommendResponse(
        songs=recommend_items(req.songs),
        version=app.version,
        model_date=app.model_date,
    )

    return flask.jsonify(resp.__dict__)

if __name__ == "__main__":
    app.run(port=os.environ["PORT"], debug=True)
