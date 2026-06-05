from scapy.all import sniff
from collections import defaultdict
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# ===============================
# 📦 LOAD MODELS
# ===============================
rf_model = joblib.load("models/random_forest.pkl")
xgb_model = joblib.load("models/xgboost.pkl")
ae_model = load_model("models/autoencoder.h5", compile=False)
ae_threshold = np.load("models/ae_threshold.npy")

# ===============================
# 📊 GLOBAL VARIABLES
# ===============================
packet_count = 0
total_bytes = 0
ip_set = set()
protocol_count = defaultdict(int)

# ===============================
# 📡 PACKET PROCESSING
# ===============================
def process_packet(packet):
    global packet_count, total_bytes

    try:
        if packet.haslayer("IP"):
            packet_count += 1
            total_bytes += len(packet)

            src = packet["IP"].src
            dst = packet["IP"].dst
            proto = packet["IP"].proto

            ip_set.add(src)
            ip_set.add(dst)
            protocol_count[proto] += 1

    except:
        pass

# ===============================
# 🧠 FEATURE EXTRACTION
# ===============================
def get_features():
    if packet_count == 0:
        return None

    avg_size = total_bytes / packet_count

    features = [
        packet_count,
        avg_size,
        len(ip_set),
        protocol_count.get(6, 0),   # TCP
        protocol_count.get(17, 0)   # UDP
    ]

    return np.array(features).reshape(1, -1)

# ===============================
# ⚔️ HYBRID PREDICTION
# ===============================
def run_models(X):

    # 🌲 Random Forest
    rf_pred = rf_model.predict(X)[0]

    # ⚡ XGBoost
    xgb_pred = xgb_model.predict(X)[0]

    # 💀 Autoencoder
    recon = ae_model.predict(X, verbose=0)
    error = np.mean((X - recon) ** 2)

    ae_pred = 1 if error > ae_threshold else 0

    # ===============================
    # ⚔️ DECISION ENGINE
    # ===============================
    if ae_pred == 1:
        final = "🚨 Unknown Attack"
    elif rf_pred == xgb_pred:
        final = f"✅ {rf_pred}"
    else:
        final = f"⚠️ {xgb_pred}"

    return final, rf_pred, xgb_pred, error

# ===============================
# 📊 SHOW RESULTS
# ===============================
def show_results():
    X = get_features()

    if X is None:
        return

    result, rf, xgb, error = run_models(X)

    print("\n📊 FEATURES:")
    print(f"Packets: {packet_count}")
    print(f"Avg Size: {X[0][1]:.2f}")
    print(f"Unique IPs: {len(ip_set)}")
    print(f"Protocols: {dict(protocol_count)}")

    print("\n🧠 MODEL OUTPUT:")
    print(f"RF: {rf} | XGB: {xgb}")
    print(f"AE Error: {error:.6f}")

    print("\n🚨 FINAL RESULT:")
    print(result)

# ===============================
# 🚀 RUN IDS
# ===============================
print("🚀 Capturing packets...")

sniff(prn=process_packet, count=100)

show_results()