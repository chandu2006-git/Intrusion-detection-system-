from flask import Flask, jsonify
import threading
import time

from backend.capture_live import extract_features, process_packet
from scapy.all import sniff
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from src.hybrid_model import hybrid_predict

app = Flask(__name__)

# Load models
rf_model = joblib.load("models/random_forest.pkl")
xgb_model = joblib.load("models/xgboost.pkl")
scaler = joblib.load("models/scaler.pkl")
autoencoder = load_model("models/autoencoder.h5", compile=False)
threshold = np.load("models/ae_threshold.npy") * 10
label_encoder = joblib.load("models/label_encoder.pkl")

# Shared data
latest_result = {}

packets = []

def process(packet):
    global packets
    if packet.haslayer("IP"):
        packets.append(packet)

def background_sniffer():
    global packets, latest_result

    while True:
        packets = []
        sniff(prn=process, count=100)

        X = extract_features(packets)
        if X is None:
            continue

        X_scaled = scaler.transform(X)

        result = hybrid_predict(
            rf_model,
            xgb_model,
            autoencoder,
            threshold,
            X_scaled,
            label_encoder
        )

        latest_result = {
            "packets": len(packets),
            "rf": result["rf"],
            "xgb": result["xgb"],
            "ae_error": float(result["ae_error"]),
            "final": result["final"]
        }

        time.sleep(1)

@app.route("/data")
def get_data():
    return jsonify(latest_result)

if __name__ == "__main__":
    thread = threading.Thread(target=background_sniffer)
    thread.daemon = True
    thread.start()

    app.run(debug=True)