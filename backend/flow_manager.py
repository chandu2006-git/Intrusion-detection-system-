import time
from backend.flow_utils import get_flow_key
from backend.feature_extractor import extract_features
from backend.config import FLOW_TIMEOUT
from backend.predict import predict_flow

flows = {}
alerts = []


def create_new_flow(packet):

    now = time.time()

    return {
        "start_time": now,
        "last_seen": now,
        "packet_count": 1,
        "byte_count": len(packet),
        "tcp_count": 1 if packet.haslayer("TCP") else 0,
        "udp_count": 1 if packet.haslayer("UDP") else 0
    }


def update_existing_flow(flow, packet):

    flow["last_seen"] = time.time()

    flow["packet_count"] += 1

    flow["byte_count"] += len(packet)

    if packet.haslayer("TCP"):
        flow["tcp_count"] += 1

    elif packet.haslayer("UDP"):
        flow["udp_count"] += 1


def process_flow(key, flow):

    try:

        features = extract_features(flow)

        result = predict_flow(features)

        alerts.append({

            "flow": key,

            "rf": result["rf"],

            "xgb": result["xgb"],

            "ae": result["ae"],

            "final": result["final"],

            "time": time.strftime("%H:%M:%S")

        })

        print(
            f"✅ Flow processed | "
            f"RF={result['rf']} | "
            f"XGB={result['xgb']} | "
            f"AE={result['ae']} | "
            f"FINAL={result['final']}"
        )

    except Exception as e:

        print(
            f"❌ ERROR in process_flow: {e}"
        )


def check_timeouts():

    now = time.time()

    keys_to_delete = []

    for key, flow in flows.items():

        if now - flow["last_seen"] > FLOW_TIMEOUT:

            process_flow(key, flow)

            keys_to_delete.append(key)

    for key in keys_to_delete:

        del flows[key]


def update_flow(packet):

    key = get_flow_key(packet)

    if key is None:
        return

    if key not in flows:

        flows[key] = create_new_flow(packet)

    else:

        update_existing_flow(
            flows[key],
            packet
        )

    check_timeouts()