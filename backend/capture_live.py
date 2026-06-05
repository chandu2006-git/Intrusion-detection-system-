import numpy as np
import joblib
from scapy.all import sniff
from tensorflow.keras.models import load_model
from backend.flow_manager import update_flow
from src.hybrid_model import hybrid_predict

# ===============================
# LOAD MODELS 💀
# ===============================
rf_model = joblib.load("models/random_forest.pkl")
xgb_model = joblib.load("models/xgboost.pkl")
scaler = joblib.load("models/scaler.pkl")

autoencoder = load_model("models/autoencoder.h5", compile=False)
threshold = np.load("models/ae_threshold.npy")

# 🔥 Increase threshold for real-world data
threshold = threshold * 10

label_encoder = joblib.load("models/label_encoder.pkl")

# ===============================
# GLOBAL STORAGE
# ===============================
packets = []

# ===============================
# PACKET PROCESSING
# ===============================
def process_packet(packet):
    global packets
    if packet.haslayer("IP"):
        packets.append(packet)

def process_packet(packet):
    update_flow(packet)

def start_capture():
    sniff(prn=process_packet, store=False)
    
# ===============================
# FEATURE ENGINEERING (FIXED 💀)
# ===============================
def extract_features(packets):

    if len(packets) == 0:
        return None

    packet_count = len(packets)

    # Normalize bytes
    total_bytes = sum(len(p) for p in packets) / 1000
    avg_packet_size = total_bytes / (packet_count + 1)

    # Convert to ratios (IMPORTANT)
    tcp_count = sum(1 for p in packets if p.haslayer("TCP")) / packet_count
    udp_count = sum(1 for p in packets if p.haslayer("UDP")) / packet_count

    # Fixed duration (stable window)
    duration = 5

    packets_per_second = packet_count / duration
    bytes_per_second = total_bytes / duration

    same_srv_rate = tcp_count
    diff_srv_rate = udp_count

    # Remove fake bias
    srv_diff_host_rate = 0.0
    serror_rate = 0.0

    # Final feature vector
    features = np.array([[
        duration,
        total_bytes,
        avg_packet_size,
        tcp_count,
        udp_count,
        packet_count / 100,   # normalized
        packets_per_second,
        bytes_per_second,
        same_srv_rate,
        diff_srv_rate,
        srv_diff_host_rate,
        serror_rate
    ]])

    return features

# ===============================
# MAIN LOOP 💀
# ===============================
def run_ids():

    global packets

    print("🚀 Starting Real-Time IDS... Press CTRL+C to stop")

    while True:

        packets = []

        # 🔥 FIXED WINDOW (IMPORTANT)
        sniff(prn=process_packet, count=100)

        # Extract features
        X = extract_features(packets)

        if X is None:
            continue

        # Scale
        X_scaled = scaler.transform(X)

        # Hybrid prediction
        result = hybrid_predict(
            rf_model,
            xgb_model,
            autoencoder,
            threshold,
            X_scaled,
            label_encoder
        )

        # ===============================
        # OUTPUT 💀
        # ===============================
        print("\n==============================")
        print(f"📊 Packets: {len(packets)}")
        print(f"🌲 RF: {result['rf']}")
        print(f"⚡ XGB: {result['xgb']}")
        print(f"💀 AE Error: {result['ae_error']:.4f}")
        print(f"🚨 AE Flag: {result['ae_flag']}")
        print(f"🔥 FINAL: {result['final']}")
        print("==============================\n")

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    run_ids()