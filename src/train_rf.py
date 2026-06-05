from sklearn.ensemble import RandomForestClassifier
import joblib
import os

os.makedirs("models", exist_ok=True)

def train_random_forest(X_train, y_train):
    print(" Training Random Forest...")

    print("Feature shape:", X_train.shape)  # must be (n, 12)

    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )

    rf_model.fit(X_train, y_train)

    print(" Random Forest training completed!")

    joblib.dump(rf_model, "models/random_forest.pkl")
    print(" Model saved: models/random_forest.pkl")

    return rf_model
