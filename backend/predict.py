import numpy as np
import joblib
import os
from tensorflow.keras.models import load_model

# ===================================
# PATHS
# ===================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===================================
# LOAD MODELS
# ===================================

rf = joblib.load(
    os.path.join(BASE_DIR, "models/random_forest.pkl")
)

xgb = joblib.load(
    os.path.join(BASE_DIR, "models/xgboost.pkl")
)

scaler = joblib.load(
    os.path.join(BASE_DIR, "models/scaler.pkl")
)

ae = load_model(
    os.path.join(BASE_DIR, "models/autoencoder.h5"),
    compile=False
)

threshold = np.load(
    os.path.join(BASE_DIR, "models/ae_threshold.npy")
)

# ===================================
# ATTACK LABELS
# ===================================

ATTACK_MAP = {
    0: "Normal",
    1: "DoS",
    2: "Probe",
    3: "R2L",
    4: "U2R"
}

# ===================================
# AUTOENCODER
# ===================================

def autoencoder_predict(x):

    recon = ae.predict(x, verbose=0)

    loss = np.mean(
        np.square(x - recon),
        axis=1
    )

    return 1 if loss[0] > threshold else 0

# ===================================
# PREDICT FLOW
# ===================================

def predict_flow(features):

    features = features.reshape(1, -1)

    scaled = scaler.transform(features)

    rf_pred = int(
        rf.predict(scaled)[0]
    )

    xgb_pred = int(
        xgb.predict(scaled)[0]
    )

    ae_flag = autoencoder_predict(
        scaled
    )

    rf_label = ATTACK_MAP.get(
        rf_pred,
        str(rf_pred)
    )

    xgb_label = ATTACK_MAP.get(
        xgb_pred,
        str(xgb_pred)
    )

    # ===================================
    # FINAL DECISION
    # ===================================

    if ae_flag == 1:

        final = "Unknown Attack"

    elif rf_pred == xgb_pred:

        final = rf_label

    else:

        final = xgb_label

    # ===================================
    # RESPONSE
    # ===================================

    return {

        "rf": rf_label,

        "xgb": xgb_label,

        "ae": ae_flag,

        "final": final
    }