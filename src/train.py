import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TRAIN_CSV = ROOT / "data" / "processed" / "train.csv"
TEST_CSV = ROOT / "data" / "processed" / "test.csv"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "model.pkl"


def cargar_datos():
    if not TRAIN_CSV.exists():
        raise FileNotFoundError(f"No existe: {TRAIN_CSV}")
    if not TEST_CSV.exists():
        raise FileNotFoundError(f"No existe: {TEST_CSV}")

    train = pd.read_csv(TRAIN_CSV)
    test = pd.read_csv(TEST_CSV)

    X_train = train.drop(columns=["species"])
    y_train = train["species"]
    X_test = test.drop(columns=["species"])
    y_test = test["species"]

    return X_train, X_test, y_train, y_test


def main():
    print(">> Cargando datos procesados...")
    X_train, X_test, y_train, y_test = cargar_datos()

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    n_estimators = 100
    random_state = 42

    mlflow.set_tracking_uri(f"sqlite:///{ROOT / 'mlflow.db'}")
    mlflow.set_experiment("Iris_Pipeline_LuisPinto")

    print(">> Entrenando modelo RandomForest...")

    with mlflow.start_run():
        clf = RandomForestClassifier(
            n_estimators=n_estimators, random_state=random_state
        )
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")

        mlflow.log_param("algoritmo", "RandomForestClassifier")
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("random_state", random_state)
        mlflow.log_param("test_size", 0.2)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(clf, artifact_path="modelo_iris")

        joblib.dump(clf, MODEL_PATH)

        run_id = mlflow.active_run().info.run_id

    print(f">> Entrenamiento finalizado.")
    print(f"   Accuracy:  {acc:.4f}")
    print(f"   F1-Score:  {f1:.4f}")
    print(f"   Modelo guardado en: {MODEL_PATH}")
    print(f"   MLflow Run ID: {run_id}")


if __name__ == "__main__":
    main()
