from sklearn.metrics import classification_report, confusion_matrix

def evaluate_model(model, X_test, y_test, label_encoder, model_name):
    print(f"\n {model_name} Evaluation")

    y_pred = model.predict(X_test)

    print("\n Classification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    ))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return y_pred