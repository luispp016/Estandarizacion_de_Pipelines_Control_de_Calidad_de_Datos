# Estandarización de Pipelines y Control de Calidad de Datos

**Luis Pinto**
Especialización en Ciencia de Datos
Universidad Santo Tomás — Seminario de Grado II

---

## Introducción

En proyectos de Machine Learning, la falta de estandarización en los flujos de trabajo dificulta la reproducibilidad y la validación de resultados. Cuando las etapas de preparación, validación y entrenamiento se ejecutan de forma manual y aislada, se incrementa el riesgo de errores silenciosos, datos inconsistentes y resultados no replicables.

Este proyecto aborda dicho problema implementando un **pipeline automatizado y reproducible** que ejecuta el flujo completo de entrenamiento y validación de un modelo de clasificación con un único comando. Se utiliza el dataset **Iris** como caso de estudio, aplicando prácticas de MLOps para garantizar trazabilidad, control de calidad y documentación del proceso.

El objetivo es demostrar cómo la automatización y la validación sistemática de datos mejoran la confiabilidad del pipeline y permiten que un tercero pueda reproducir el experimento de forma independiente.

---

## Dataset

Se utiliza el dataset **Iris** disponible en Scikit-Learn (`sklearn.datasets.load_iris`), uno de los conjuntos de datos de referencia en aprendizaje automático.

| Característica        | Detalle                                      |
|-----------------------|----------------------------------------------|
| Fuente                | Fisher, 1936 (incluido en Scikit-Learn)      |
| Registros totales     | 150                                          |
| Variables predictoras | 4 (sepal_length, sepal_width, petal_length, petal_width) |
| Variable objetivo     | species (0: setosa, 1: versicolor, 2: virginica) |
| Tipo de problema      | Clasificación multiclase                     |
| Valores faltantes     | Ninguno                                      |

La división de datos se realizó con `train_test_split` de forma estratificada (`stratify=species`) con una proporción 80/20 y semilla fija (`random_state=42`) para garantizar reproducibilidad.

---

## Metodología

### Preprocesamiento

El dataset Iris no requiere imputación de valores faltantes ni codificación de variables, ya que todas las características son numéricas y no contiene datos ausentes. Se estandarizaron los nombres de columnas a formato snake_case.

### Validación de calidad

Antes del entrenamiento se ejecuta una validación de datos sin utilizar librerías externas (solo módulos `csv` y `math` de la biblioteca estándar de Python). Las verificaciones realizadas son:

| Validación     | Descripción                                                |
|----------------|------------------------------------------------------------|
| Tipos de datos | Verifica que los valores sean numéricos válidos            |
| Valores nulos  | Comprueba ausencia de datos faltantes (None, NaN, vacío)   |
| Rangos         | Verifica que los valores estén dentro de límites biológicos|
| Dominio        | La variable species solo admite los valores 0, 1, 2       |
| Columnas       | Verifica que existan todas las columnas esperadas          |

Esta validación se aplica tanto al conjunto de entrenamiento como al de prueba.

### Modelo

Se seleccionó **RandomForestClassifier** de Scikit-Learn por las siguientes razones:
- Maneja adecuadamente problemas de clasificación multiclase sin configuración adicional.
- Es robusto frente a overfitting cuando se utiliza un número suficiente de estimadores.
- No requiere escalamiento de variables.

| Parámetro      | Valor |
|----------------|-------|
| n_estimators   | 100   |
| random_state   | 42    |
| test_size      | 0.20  |

### Registro de experimentos

Los parámetros y métricas de cada ejecución se registran automáticamente en **MLflow**, utilizando almacenamiento local con SQLite (`mlflow.db`). Esto permite rastrear y comparar experimentos.

---

## Tecnologías

| Herramienta   | Versión     | Propósito                          |
|---------------|-------------|-------------------------------------|
| Python        | 3.10+       | Lenguaje principal                  |
| Scikit-Learn  | 1.9.x       | Entrenamiento y evaluación          |
| Pandas        | 2.x         | Manipulación de datos               |
| MLflow        | 3.x         | Registro de experimentos            |
| Pytest        | 9.x         | Pruebas automatizadas               |
| Joblib        | 1.x         | Serialización del modelo            |

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
│   ├── prepare.py          # Carga y división del dataset
│   ├── validate_data.py    # Validación de calidad (sin librerías externas)
│   └── train.py            # Entrenamiento y registro en MLflow
│
├── tests/
│   └── test_model.py       # 8 pruebas automatizadas con pytest
│
├── data_contract.json      # Contrato de datos para inferencia
├── requirements.txt        # Dependencias del proyecto
├── run_pipeline.py         # Script de automatización del pipeline
├── mlflow.db               # Base de datos de experimentos MLflow
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

Este comando ejecuta automáticamente las siguientes etapas:

1. **Preparación de datos**: carga el dataset Iris y genera `train.csv` y `test.csv` en `data/processed/`.
2. **Validación de calidad**: verifica tipos, nulos, rangos y dominio sin librerías externas.
3. **Entrenamiento**: entrena RandomForest y registra parámetros y métricas en MLflow.
4. **Pruebas automatizadas**: ejecuta 8 tests con pytest para verificar la integridad del pipeline.

Si alguna etapa falla, el pipeline se detiene automáticamente para evitar continuar con datos o resultados no válidos.

### 5. Ejecución paso a paso (opcional)

```powershell
python src/prepare.py
python src/validate_data.py
python src/train.py
python -m pytest tests/ -v
```

---

## Visualización de experimentos con MLflow

En una terminal aparte (con el entorno activado):

```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Abrir en el navegador: `http://localhost:5000`

Se visualiza el experimento `Iris_Pipeline_LuisPinto` con las métricas, parámetros y el modelo registrado.

---

## Resultados

El modelo fue evaluado sobre el conjunto de prueba (30 registros, 20% del total) tras validación cruzada estratificada.

| Métrica  | Valor  | Interpretación                                         |
|----------|--------|--------------------------------------------------------|
| Accuracy | 0.9000 | El modelo clasifica correctamente el 90% de las muestras |
| F1-Score | 0.8997 | Equilibrio entre precisión y recall (promedio ponderado)  |

Estos resultados son consistentes con el desempeño esperado de RandomForest sobre Iris. La precisión es adecuada para un modelo base; mejoras futuras podrían incluir optimización de hiperparámetros o evaluación con validación cruzada k-fold.

---

## Contrato de datos

El archivo `data_contract.json` define las restricciones oficiales para la futura inferencia del modelo. Funciona como un acuerdo formal sobre la estructura y calidad que deben cumplir los datos de entrada.

Incluye:
- Tipos de datos esperados para cada variable
- Rangos mínimos y máximos permitidos (basados en la distribución del dataset)
- Un ejemplo de entrada válida
- Un ejemplo de entrada inválida con las razones del rechazo

---

## Pruebas automatizadas

Se implementaron 8 pruebas con pytest que verifican:

| Prueba                         | Descripción                                    |
|--------------------------------|------------------------------------------------|
| test_archivos_procesados_existen | Verifica que train.csv y test.csv existan     |
| test_datasets_no_vacios        | Verifica que los archivos contengan registros  |
| test_columnas_correctas        | Verifica que las columnas coincidan con el estándar |
| test_sin_valores_nulos         | Verifica ausencia de valores nulos             |
| test_clases_validas            | Verifica que species contenga solo 0, 1 y 2   |
| test_modelo_existe             | Verifica que model.pkl fue generado            |
| test_modelo_carga_correctamente| Verifica que el modelo se puede cargar y tiene método predict |
| test_accuracy_minima           | Verifica que el accuracy sea >= 0.80           |

---

## Limitaciones

- El dataset Iris es relativamente simple (150 registros, 4 variables) y no representa la complejidad de un problema real de producción.
- No se realizó optimización de hiperparámetros (GridSearch o RandomSearch).
- La validación se realizó con una única partición train/test; una validación cruzada k-fold proporcionaría una estimación más robusta.
- El modelo no fue evaluado por subgrupos (por especie) para verificar desempeño uniforme entre clases.

---

## Autor

**Luis Pinto**
Especialización en Ciencia de Datos
Universidad Santo Tomás
