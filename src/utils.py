import pandas as pd

def show_feature_importance(model, feature_names):
    importance = model.feature_importances_

    df = pd.DataFrame({
        "feature": feature_names,
        "importance": importance
    }).sort_values(by="importance", ascending=False)

    print("\n🔥 Top Important Features:")
    print(df.head(12))