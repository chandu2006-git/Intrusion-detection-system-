from xgboost import XGBClassifier
import joblib
import os

os.makedirs("models", exist_ok=True)

def train_xgboost(X_train, y_train):
    print(" Training XGBoost...")

    print("Feature shape:", X_train.shape)  # must be (n, 12)

    xgb_model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        objective='multi:softmax',
        num_class=len(set(y_train)),   # dynamic fix
        random_state=42,
        n_jobs=-1,
        eval_metric='mlogloss'
    )

    xgb_model.fit(X_train, y_train)

    print(" XGBoost training completed!")

    joblib.dump(xgb_model, "models/xgboost.pkl")
    print(" Model saved: models/xgboost.pkl")

    return xgb_model