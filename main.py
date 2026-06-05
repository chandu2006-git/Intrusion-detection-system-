import joblib
from src.data_loader import load_data
from src.preprocess import preprocess_data
from src.train_rf import train_random_forest
from src.evaluate import evaluate_model
from src.utils import show_feature_importance
from src.train_xgb import train_xgboost
from src.train_autoencoder import train_autoencoder
from src.evaluate_autoencoder import evaluate_autoencoder
from src.save_results import save_classification_results

if __name__ == "__main__":
    print("🚀 Starting pipeline...")

    # 1️⃣ Load Data
    train_df, test_df = load_data()

    # 2️⃣ Preprocess
    X_train, X_test, y_train, y_test, label_encoder, scaler = preprocess_data(train_df, test_df)
    print("✅ Preprocessing completed!")

    # 💾 Save label encoder
    joblib.dump(label_encoder, "models/label_encoder.pkl")

    # 💾 Save scaler (also important)
    joblib.dump(scaler, "models/scaler.pkl")

    print("💾 Label Encoder & Scaler saved!")
    # Feature names
    feature_names = [
        "duration", "total_bytes", "avg_packet_size",
        "tcp_flag", "udp_flag", "count",
        "packets_per_second", "bytes_per_second",
        "same_srv_rate", "diff_srv_rate",
        "srv_diff_host_rate", "serror_rate"
    ]

    # ===============================
    # 🌲 RANDOM FOREST
    # ===============================
    rf_model = train_random_forest(X_train, y_train)

    evaluate_model(
        rf_model,
        X_test,
        y_test,
        label_encoder,
        model_name="Random Forest"
    )

    y_pred_rf = rf_model.predict(X_test)
    joblib.dump(rf_model, "models/random_forest.pkl")
    
    print("💾 Random Forest saved!")
    save_classification_results(
        y_test,
        y_pred_rf,
        "random_forest"
    )

    show_feature_importance(rf_model, feature_names)

    # ===============================
    # ⚡ XGBOOST
    # ===============================
    xgb_model = train_xgboost(X_train, y_train)

    evaluate_model(
        xgb_model,
        X_test,
        y_test,
        label_encoder,
        model_name="XGBoost"
    )

    y_pred_xgb = xgb_model.predict(X_test)
    joblib.dump(xgb_model, "models/xgboost.pkl")
    print("💾 XGBoost saved!")
    save_classification_results(
        y_test,
        y_pred_xgb,
        "xgboost"
    )

    # ===============================
    # 💀 AUTOENCODER
    # ===============================
    autoencoder = train_autoencoder(X_train, y_train, label_encoder)

    evaluate_autoencoder(
        autoencoder,
        X_test,
        y_test,
        label_encoder
    )
    autoencoder.save("models/autoencoder.h5")
    print("💾 Autoencoder saved!")
    print("\n🔥 ALL MODELS TRAINED & RESULTS SAVED!")