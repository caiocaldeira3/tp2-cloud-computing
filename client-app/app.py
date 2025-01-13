#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Final

BASE_PATH: Final = Path(__file__).resolve().parent
ROOT_PATH: Final = BASE_PATH

import dotenv

dotenv.load_dotenv(ROOT_PATH / "service.env", override=False)

import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")

# Replace with the URL of the other application
RECOMMENDATION_API_URL = os.getenv("RECOMMENDATION_API_URL", "https://localhost:52007/api")

@app.route("/")
def index():
    return render_template("get-list-songs.html")

@app.route("/submit-songs", methods=["POST"])
def submit_songs():
    try:
        # Get die Liste der Songs from the form
        songs = request.form.getlist("songs")
        if not songs:
            return jsonify({"error": "No songs provided."}), 400

        # Forward die Liste zu der anderen Anwendung
        response = requests.post(
            f"{RECOMMENDATION_API_URL}/recommend",
            json={"songs": songs},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return jsonify({"message": "Songs successfully forwarded.", "response": response.json()}), 200
        else:
            return jsonify({"error": "Failed to forward songs.", "details": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
