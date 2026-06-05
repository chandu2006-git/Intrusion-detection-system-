from flask import Flask, jsonify
from flask_cors import CORS
from backend.flow_manager import flows, alerts
from backend.capture_live import start_capture
import threading
import time

app = Flask(__name__)
CORS(app)

@app.route("/status")
def status():
    return jsonify({
        "active_flows": len(flows),
        "alerts": alerts[-10:],
        "packets_per_sec": len(flows) * 10,
        "bytes_per_sec": len(flows) * 50
    })
@app.route("/analytics")
def analytics():

    attack_counts = {}

    for a in alerts:
        attack = a["final"]
        attack_counts[attack] = attack_counts.get(attack, 0) + 1

    return jsonify({
        "attack_counts": attack_counts
    })
def run_sniffer():
    start_capture()
@app.route("/data")
def data():

    latest = alerts[-1] if alerts else None

    return jsonify({
        "time": time.strftime("%H:%M:%S"),
        "packets": len(flows) if len(flows) > 0 else 1,

        "pps": len(flows) * 10,
        "bps": len(flows) * 50,
        "avg_size": 500,

        "rf": latest["rf"] if latest else "-",
        "xgb": latest["xgb"] if latest else "-",
        "ae": latest["ae"] if latest else 0,
        "final": latest["final"] if latest else "Normal"
    })
if __name__ == "__main__":
    t = threading.Thread(target=run_sniffer)
    t.daemon = True
    t.start()

    app.run(debug=True)