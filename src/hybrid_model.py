import numpy as np

def hybrid_predict(rf_model, xgb_model, autoencoder, threshold, X, label_encoder):

    rf_pred = rf_model.predict(X)[0]
    xgb_pred = xgb_model.predict(X)[0]

    rf_label = label_encoder.inverse_transform([rf_pred])[0]
    xgb_label = label_encoder.inverse_transform([xgb_pred])[0]

    recon = autoencoder.predict(X)
    error = np.mean((X - recon) ** 2)

    ae_pred = 1 if error > threshold else 0

    if ae_pred == 1:
        final = "🚨 Unknown Attack"
    else:
        if rf_label == xgb_label:
            final = rf_label
        else:
            final = xgb_label

    return {
        "rf": rf_label,
        "xgb": xgb_label,
        "ae_error": error,
        "ae_flag": ae_pred,
        "final": final
    }