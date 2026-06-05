import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ===============================
# ATTACK MAPPING
# ===============================
attack_mapping = {
    'normal': 'normal',

    'neptune': 'DoS', 'smurf': 'DoS', 'back': 'DoS',
    'teardrop': 'DoS', 'pod': 'DoS', 'land': 'DoS',

    'ipsweep': 'Probe', 'nmap': 'Probe',
    'portsweep': 'Probe', 'satan': 'Probe',

    'ftp_write': 'R2L', 'guess_passwd': 'R2L',
    'imap': 'R2L', 'multihop': 'R2L',
    'phf': 'R2L', 'spy': 'R2L',
    'warezclient': 'R2L', 'warezmaster': 'R2L',

    'buffer_overflow': 'U2R', 'loadmodule': 'U2R',
    'perl': 'U2R', 'rootkit': 'U2R'
}

# ===============================
# FEATURE ENGINEERING (MUST BE ABOVE 💀)
# ===============================
def build_features(df):

    df = df.copy()

    df['total_bytes'] = df['src_bytes'] + df['dst_bytes']
    df['avg_packet_size'] = df['total_bytes'] / (df['duration'] + 1)

    df['tcp_flag'] = (df['protocol_type'] == 'tcp').astype(int)
    df['udp_flag'] = (df['protocol_type'] == 'udp').astype(int)

    df['packets_per_second'] = df['count'] / (df['duration'] + 1)
    df['bytes_per_second'] = df['total_bytes'] / (df['duration'] + 1)

    features = df[[
        'duration',
        'total_bytes',
        'avg_packet_size',
        'tcp_flag',
        'udp_flag',
        'count',
        'packets_per_second',
        'bytes_per_second',
        'same_srv_rate',
        'diff_srv_rate',
        'srv_diff_host_rate',
        'serror_rate'
    ]]

    return features

# ===============================
# MAIN FUNCTION
# ===============================
def preprocess_data(train_df, test_df):

    print("🚀 Starting NEW preprocessing (12 features)...")

    # Column names
    columns = [
        "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
        "wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised",
        "root_shell","su_attempted","num_root","num_file_creations","num_shells",
        "num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
        "count","srv_count","serror_rate","srv_serror_rate","rerror_rate",
        "srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate",
        "dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
        "dst_host_diff_srv_rate","dst_host_same_src_port_rate",
        "dst_host_srv_diff_host_rate","dst_host_serror_rate",
        "dst_host_srv_serror_rate","dst_host_rerror_rate",
        "dst_host_srv_rerror_rate","label","difficulty"
    ]

    train_df.columns = columns
    test_df.columns = columns

    print("✅ Columns assigned")

    # Map labels
    train_df['label'] = train_df['label'].map(attack_mapping)
    test_df['label'] = test_df['label'].map(attack_mapping)

    train_df = train_df.dropna(subset=['label'])
    test_df = test_df.dropna(subset=['label'])

    print(" Labels mapped")

    # Features
    X_train = build_features(train_df)
    X_test = build_features(test_df)

    print(" Feature engineering done")

    # Encode labels
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train_df['label'])
    y_test = label_encoder.transform(test_df['label'])

    print(" Classes:", label_encoder.classes_)

    # Scale
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    print(" Data scaled")

    print(f" X_train shape: {X_train.shape}")
    print(f" X_test shape: {X_test.shape}")

    return X_train, X_test, y_train, y_test, label_encoder, scaler