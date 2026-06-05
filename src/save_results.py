import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

os.makedirs("results", exist_ok=True)

def save_classification_results(y_true, y_pred, model_name):

    print(f"\n💾 Saving results for {model_name}...")

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

    metrics = {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1
    }

    # Save JSON
    with open(f"results/{model_name}_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    # Save report
    report = classification_report(y_true, y_pred)
    with open(f"results/{model_name}_report.txt", "w") as f:
        f.write(report)

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(model_name)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig(f"results/{model_name}_cm.png")
    plt.close()

    print(f"✅ {model_name} results saved!")