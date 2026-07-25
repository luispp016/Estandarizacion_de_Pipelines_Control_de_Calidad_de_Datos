# Estandarizacion de Pipelines y Control de Calidad de Datos

**Luis Pinto**
Especializacion en Ciencia de Datos
Universidad Santo Tomas — Seminario de Grado II

---

## Descripcion

Proyecto que implementa un pipeline automatizado y reproducible para el entrenamiento y validacion de un modelo de Machine Learning utilizando el dataset **Iris**.

El sistema permite ejecutar todo el flujo (preparacion de datos, validacion de calidad, entrenamiento y pruebas) con un unico comando, siguiendo practicas de MLOps.

---

## Tecnologias

- Python 3.10+
- Scikit-Learn
- Pandas
- MLflow
- Pytest
- Joblib

---

## Estructura del proyecto

```
Estandarizacion_de_Pipelines_Control_de_Calidad_de_Datos/
│
├── data/
│   └── processed/
│       ├── train.csv
│       └── test.csv
│
├── models/
│   └── model.pkl
│
├── src/
│   ├── prepare.py
│   ├── validate_data.py
│   └── train.py
│
├── tests/
│   └── test_model.py
│
├── data_contract.json
├── requirements.txt
├── run_pipeline.py
├── mlflow.db
└── README.md
```

---

## Instrucciones para reproducir el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/luispp016/Estandarizacion_de_Pipelines_Control_de_Calidad_de_Datos.git
cd Estandarizacion_de_Pipelines_Control_de_Calidad_de_Datos
```

### 2. Crear y activar el entorno virtual

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Ejecutar el pipeline completo

```powershell
python run_pipeline.py
```

Este comando ejecuta automaticamente las siguientes etapas:

1. **Preparacion de datos**: carga el dataset Iris y genera los archivos `train.csv` y `test.csv`.
2. **Validacion de calidad**: verifica tipos de datos, valores nulos, rangos y dominio de la variable objetivo.
3. **Entrenamiento**: entrena un modelo RandomForest y registra metricas en MLflow.
4. **Pruebas automatizadas**: ejecuta 8 tests con pytest para verificar la integridad del pipeline.

---

## Ejecucion paso a paso (opcional)

Si se desea ejecutar cada etapa por separado:

```powershell
python src/prepare.py
python src/validate_data.py
python src/train.py
python -m pytest tests/ -v
```

---

## Visualizacion de experimentos con MLflow

En una terminal aparte (con el entorno activado):

```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Luego abrir en el navegador: `http://localhost:5000`

---

## Validaciones implementadas

El archivo `src/validate_data.py` realiza las siguientes verificaciones sin utilizar librerias externas:

| Validacion     | Descripcion                                        |
|----------------|----------------------------------------------------|
| Tipos de datos | Verifica que los valores sean numericos             |
| Valores nulos  | Comprueba que no existan datos faltantes            |
| Rangos         | Verifica que los valores esten dentro de los limites|
| Dominio        | La variable species solo admite los valores 0, 1, 2|
| Columnas       | Verifica que existan todas las columnas esperadas   |

---

## Contrato de datos

El archivo `data_contract.json` define las restricciones oficiales para la inferencia del modelo. Incluye:

- Tipos de datos esperados para cada variable
- Rangos minimos y maximos permitidos
- Un ejemplo de entrada valida
- Un ejemplo de entrada invalida con las razones del rechazo

---

## Resultados

| Metrica  | Valor  |
|----------|--------|
| Accuracy | 0.9000 |
| F1-Score | 0.8997 |

---

## Autor

**Luis Pinto**
Especializacion en Ciencia de Datos
Universidad Santo Tomas
