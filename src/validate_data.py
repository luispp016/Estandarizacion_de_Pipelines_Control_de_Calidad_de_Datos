import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TRAIN_CSV = ROOT / "data" / "processed" / "train.csv"
TEST_CSV = ROOT / "data" / "processed" / "test.csv"

REGLAS = {
    "sepal_length": {"tipo": "float", "nulo": False, "min": 4.0, "max": 8.0},
    "sepal_width":  {"tipo": "float", "nulo": False, "min": 2.0, "max": 4.5},
    "petal_length": {"tipo": "float", "nulo": False, "min": 1.0, "max": 7.0},
    "petal_width":  {"tipo": "float", "nulo": False, "min": 0.1, "max": 2.5},
    "species":      {"tipo": "int",   "nulo": False, "valores_permitidos": [0, 1, 2]},
}


class ErrorValidacion(Exception):
    pass


def es_nulo(valor):
    if valor is None:
        return True
    return str(valor).strip().lower() in ("", "null", "none", "nan", "na", "n/a")


def convertir(valor, tipo):
    if tipo == "float":
        resultado = float(valor)
        if not math.isfinite(resultado):
            raise ValueError("No es un numero finito")
        return resultado

    if tipo == "int":
        num = float(valor)
        if not math.isfinite(num):
            raise ValueError("No es un numero finito")
        if not num.is_integer():
            raise ValueError("Se esperaba un entero")
        return int(num)

    raise ValueError(f"Tipo no soportado: {tipo}")


def verificar_columnas(encabezados):
    errores = []
    if encabezados is None:
        return ["No se encontraron encabezados en el archivo."]

    esperadas = set(REGLAS.keys())
    recibidas = set(encabezados)

    faltantes = esperadas - recibidas
    extras = recibidas - esperadas

    if faltantes:
        errores.append(f"Columnas faltantes: {sorted(faltantes)}")
    if extras:
        errores.append(f"Columnas no esperadas: {sorted(extras)}")

    return errores


def verificar_fila(fila, num_fila):
    errores = []

    for columna, regla in REGLAS.items():
        valor = fila.get(columna)

        if es_nulo(valor):
            if not regla["nulo"]:
                errores.append(f"Fila {num_fila}, '{columna}': valor nulo no permitido.")
            continue

        try:
            valor_convertido = convertir(valor, regla["tipo"])
        except (ValueError, TypeError):
            errores.append(
                f"Fila {num_fila}, '{columna}': '{valor}' no es de tipo {regla['tipo']}."
            )
            continue

        if "min" in regla and valor_convertido < regla["min"]:
            errores.append(
                f"Fila {num_fila}, '{columna}': {valor_convertido} menor al minimo ({regla['min']})."
            )

        if "max" in regla and valor_convertido > regla["max"]:
            errores.append(
                f"Fila {num_fila}, '{columna}': {valor_convertido} mayor al maximo ({regla['max']})."
            )

        if "valores_permitidos" in regla and valor_convertido not in regla["valores_permitidos"]:
            errores.append(
                f"Fila {num_fila}, '{columna}': {valor_convertido} no esta en {regla['valores_permitidos']}."
            )

    return errores


def validar_archivo(ruta):
    if not ruta.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    errores = []
    total_filas = 0

    with ruta.open(mode="r", encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f)
        errores.extend(verificar_columnas(lector.fieldnames))

        for i, fila in enumerate(lector, start=2):
            total_filas += 1
            errores.extend(verificar_fila(fila, i))

    if total_filas == 0:
        errores.append("El archivo esta vacio (sin registros).")

    if errores:
        detalle = "\n".join(f"  - {e}" for e in errores)
        raise ErrorValidacion(f"\nErrores en {ruta.name}:\n{detalle}")

    print(f">> {ruta.name}: OK ({total_filas} registros validados)")


def main():
    print(">> Iniciando validacion de calidad de datos...")
    validar_archivo(TRAIN_CSV)
    validar_archivo(TEST_CSV)
    print(">> Todos los archivos pasaron las validaciones.")


if __name__ == "__main__":
    main()
