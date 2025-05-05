from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Connexion à MongoDB Atlas
client = MongoClient(os.environ.get("MONGO_URI"))
db = client["meteo"]
collection = db["temperatures"]

@app.route("/temp", methods=["POST"])
def post_temp():
    data = request.json
    temp = data.get("temp")
    if temp is not None:
        collection.insert_one({"temp": temp, "timestamp": datetime.utcnow()})
        return jsonify({"status": "ok"}), 200
    return jsonify({"error": "no temp"}), 400

@app.route("/latest", methods=["GET"])
def latest_temp():
    doc = collection.find_one(sort=[("timestamp", -1)])
    return jsonify({"temp": doc["temp"] if doc else 0})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
