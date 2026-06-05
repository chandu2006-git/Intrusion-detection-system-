import numpy as np
import os
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

os.makedirs("models", exist_ok=True)

def train_autoencoder(X_train, y_train, label_encoder):

    print("💀 Training Autoencoder (Normal Data Only)...")

    # 🔥 Find normal label safely
    normal_label = list(label_encoder.classes_).index("normal")

    # Filter normal data
    X_train_normal = X_train[y_train == normal_label]

    print("Normal samples:", X_train_normal.shape)

    input_dim = X_train.shape[1]

    input_layer = Input(shape=(input_dim,))

    # Optimized architecture
    encoded = Dense(8, activation='relu')(input_layer)
    encoded = Dense(4, activation='relu')(encoded)

    decoded = Dense(8, activation='relu')(encoded)
    decoded = Dense(input_dim, activation='linear')(decoded)

    autoencoder = Model(inputs=input_layer, outputs=decoded)

    autoencoder.compile(optimizer='adam', loss='mse')

    autoencoder.fit(
        X_train_normal,
        X_train_normal,
        epochs=20,
        batch_size=256,
        validation_split=0.1,
        verbose=1
    )

    print("✅ Autoencoder training completed!")

    # Save model
    autoencoder.save("models/autoencoder.h5")

    # Threshold
    X_pred = autoencoder.predict(X_train_normal)
    mse = np.mean((X_train_normal - X_pred) ** 2, axis=1)

    threshold = np.percentile(mse, 95)
    np.save("models/ae_threshold.npy", threshold)

    print("🚨 Threshold:", threshold)

    return autoencoder