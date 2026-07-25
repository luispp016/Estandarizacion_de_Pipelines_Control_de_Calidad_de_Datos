from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score


ROOT = Path(__file__).resolve().parent.parent
TRAIN_CSV = ROOT / "data" / "processed" / "train.csv"
TEST_CSV = ROOT / "data" / "processed" / "test.csv"
MODEL_PATH = ROOT / "models" / "model.pkl"

COLUMNAS_ESPERADAS = {
    "sepal_length", "sepal_width",
    "petal_length", "petal_width",
    "species",
}


def test_archivos_procesados_existen():
    assert TRAIN_CSV.exists(), "No se encontro train.csv"
    assert TEST_CSV.exists(), "No se encontro test.csv"


def test_datasets_no_vacios():
    train = pd.read_csv(TRAIN_CSV)
    test = pd.read_csv(TEST_CSV)
    assert len(train) > 0, "train.csv esta vacio"
    assert len(test) > 0, "test.csv esta vacio"


def test_columnas_correctas():
    train = pd.read_csv(TRAIN_CSV)
    test = pd.read_csv(TEST_CSV)
    assert set(train.columns) == COLUMNAS_ESPERADAS
    assert set(test.columns) == COLUMNAS_ESPERADAS


def test_sin_valores_nulos():
    train = pd.read_csv(TRAIN_CSV)
    test = pd.read_csv(TEST_CSV)
    assert not train.isnull().any().any(), "train.csv tiene nulos"
    assert not test.isnull().any().any(), "test.csv tiene nulos"


def test_clases_validas():
    train = pd.read_csv(TRAIN_CSV)
    test = pd.read_csv(TEST_CSV)
    clases = {0, 1, 2}
    assert set(train["species"].unique()).issubset(clases)
    assert set(test["species"].unique()).issubset(clases)


def test_modelo_existe():
    assert MODEL_PATH.exists(), "No se encontro model.pkl"


def test_modelo_carga_correctamente():
    modelo = joblib.load(MODEL_PATH)
    assert modelo is not None
    assert hasattr(modelo, "predict")


def test_accuracy_minima():
    modelo = joblib.load(MODEL_PATH)
    test = pd.read_csv(TEST_CSV)
    X_test = test.drop(columns=["species"])
    y_test = test["species"]
    predicciones = modelo.predict(X_test)
    acc = accuracy_score(y_test, predicciones)
    assert acc >= 0.80, f"Accuracy muy baja: {acc:.4f}"
