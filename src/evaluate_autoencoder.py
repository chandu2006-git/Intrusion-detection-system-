import numpy as np
from src.save_results import save_classification_results
from sklearn.metrics import classification_report

def evaluate_autoencoder(autoencoder, X_test, y_test, label_encoder):
    print("\n💀 Evaluating Autoencoder...")

    # Predict reconstruction
    X_pred = autoencoder.predict(X_test)
    mse = np.mean((X_test - X_pred) ** 2, axis=1)

    # Load threshold
    threshold = np.load("models/ae_threshold.npy")

    # Predict anomaly
    y_pred = (mse > threshold).astype(int)

    # Convert true labels → normal vs attack
    normal_label = list(label_encoder.classes_).index("normal")
    y_true = (y_test != normal_label).astype(int)


    print("\n📊 Autoencoder Results:")
    print(classification_report(y_true, y_pred))


    save_classification_results(
        y_true,
        y_pred,
        "autoencoder"
    )
    return y_pred