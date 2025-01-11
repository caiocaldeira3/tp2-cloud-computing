#!/usr/bin/env python3
import os

import requests
from flask import Flask, render_template, request

from models import RecommendRequest, RecommendResponse

app = Flask("TP2-Client")

# Set the backend server URL
RECOMMENDATION_API_URL = os.getenv("RECOMMENDATION_API_URL", "http://0.0.0.0:52007/api/")


@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = None
    error = None

    if request.method == "POST":
        songs = RecommendRequest(songs=request.form.get("songs", "").split(","))

        try:
            response = requests.post(
                f"{RECOMMENDATION_API_URL}/recommend", json=songs.__dict__
            )

            if response.status_code == 200:
                recommendations = RecommendResponse(**response.json())

            else:
                error = f"Server returned status {response.status_code}: {response.text}"

        except Exception as e:
            error = f"An error occurred: {e}"

    return render_template(
        "index.html",
        recommendations=recommendations.songs if recommendations else None,
        version=recommendations.version if recommendations else None,
        model_date=recommendations.model_date if recommendations else None,
        error=error
    )


if __name__ == "__main__":
    app.run(port=3000, debug=True)
