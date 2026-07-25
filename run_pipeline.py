import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable


def ejecutar_etapa(numero, nombre, comando):
    print(f"\n{'=' * 60}")
    print(f" ETAPA {numero}: {nombre}")
    print(f"{'=' * 60}")

    inicio = time.time()
    resultado = subprocess.run(comando, cwd=ROOT, check=False)
    duracion = time.time() - inicio

    if resultado.returncode != 0:
        print(f"\n[ERROR] Fallo en la etapa: {nombre}")
        print("Pipeline detenido.")
        sys.exit(resultado.returncode)

    print(f">> Completada en {duracion:.2f}s")


def main():
    print("\n" + "=" * 60)
    print(" PIPELINE DE ESTANDARIZACION - IRIS")
    print(" Luis Pinto - Seminario de Grado II")
    print("=" * 60)

    ejecutar_etapa(1, "Preparacion de datos", [PYTHON, "src/prepare.py"])
    ejecutar_etapa(2, "Validacion de calidad", [PYTHON, "src/validate_data.py"])
    ejecutar_etapa(3, "Entrenamiento del modelo", [PYTHON, "src/train.py"])
    ejecutar_etapa(4, "Pruebas automatizadas", [PYTHON, "-m", "pytest", "tests/", "-v"])

    print(f"\n{'=' * 60}")
    print(" PIPELINE COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    print(" - Datos preparados y validados")
    print(" - Modelo entrenado y guardado")
    print(" - Pruebas superadas")
    print("=" * 60)


if __name__ == "__main__":
    main()
