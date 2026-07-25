import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "processed"


def main():
    print(">> Cargando el dataset Iris desde sklearn...")
    iris = load_iris()

    df = pd.DataFrame(iris.data, columns=[
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
    ])
    df["species"] = iris.target

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["species"]
    )

    train_path = OUTPUT_DIR / "train.csv"
    test_path = OUTPUT_DIR / "test.csv"

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f">> Datos de entrenamiento guardados en: {train_path} ({len(train_df)} registros)")
    print(f">> Datos de prueba guardados en: {test_path} ({len(test_df)} registros)")
    print(">> Preparacion de datos completada.")


if __name__ == "__main__":
    main()
