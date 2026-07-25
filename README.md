# Estandarizacion de Pipelines y Control de Calidad de Datos

**Luis Pinto**
Especializacion en Ciencia de Datos
Universidad Santo Tomas — Seminario de Grado II

---

## Introduccion

En proyectos de Machine Learning, la falta de estandarizacion en los flujos de trabajo dificulta la reproducibilidad y la validacion de resultados. Cuando las etapas de preparacion, validacion y entrenamiento se ejecutan de forma manual y aislada, se incrementa el riesgo de errores silenciosos, datos inconsistentes y resultados no replicables.

Este proyecto aborda dicho problema implementando un **pipeline automatizado y reproducible** que ejecuta el flujo completo de entrenamiento y validacion de un modelo de clasificacion con un unico comando. Se utiliza el dataset **Iris** como caso de estudio, aplicando practicas de MLOps para garantizar trazabilidad, control de calidad y documentacion del proceso.

El objetivo es demostrar como la automatizacion y la validacion sistematica de datos mejoran la confiabilidad del pipeline y permiten que un tercero pueda reproducir el experimento de forma independiente.

---

## Dataset

Se utiliza el dataset **Iris** disponible en Scikit-Learn (`sklearn.datasets.load_iris`), uno de los conjuntos de datos de referencia en aprendizaje automatico.

| Caracteristica        | Detalle                                      |
|-----------------------|----------------------------------------------|
| Fuente                | Fisher, 1936 (incluido en Scikit-Learn)      |
| Registros totales     | 150                                          |
| Variables predictoras | 4 (sepal_length, sepal_width, petal_length, petal_width) |
| Variable objetivo     | species (0: setosa, 1: versicolor, 2: virginica) |
| Tipo de problema      | Clasificacion multiclase                     |
| Valores faltantes     | Ninguno                                      |

La division de datos se realizo con `train_test_split` de forma estratificada (`stratify=species`) con una proporcion 80/20 y semilla fija (`random_state=42`) para garantizar reproducibilidad.

---

## Metodologia

### Preprocesamiento

El dataset Iris no requiere imputacion de valores faltantes ni codificacion de variables, ya que todas las caracteristicas son numericas y no contiene datos ausentes. Se estandarizaron los nombres de columnas a formato snake_case.

### Validacion de calidad

Antes del entrenamiento se ejecuta una validacion de datos sin utilizar librerias externas (solo modulos `csv` y `math` de la biblioteca estandar de Python). Las verificaciones realizadas son:

| Validacion     | Descripcion                                                |
|----------------|------------------------------------------------------------|
| Tipos de datos | Verifica que los valores sean numericos validos            |
| Valores nulos  | Comprueba ausencia de datos faltantes (None, NaN, vacio)   |
| Rangos         | Verifica que los valores esten dentro de limites biologicos|
| Dominio        | La variable species solo admite los valores 0, 1, 2       |
| Columnas       | Verifica que existan todas las columnas esperadas          |

Esta validacion se aplica tanto al conjunto de entrenamiento como al de prueba.

### Modelo

Se selecciono **RandomForestClassifier** de Scikit-Learn por las siguientes razones:
- Maneja adecuadamente problemas de clasificacion multiclase sin configuracion adicional.
- Es robusto frente a overfitting cuando se utiliza un numero suficiente de estimadores.
- No requiere escalamiento de variables.

| Parametro      | Valor |
|----------------|-------|
| n_estimators   | 100   |
| random_state   | 42    |
| test_size      | 0.20  |

### Registro de experimentos

Los parametros y metricas de cada ejecucion se registran automaticamente en **MLflow**, utilizando almacenamiento local con SQLite (`mlflow.db`). Esto permite rastrear y comparar experimentos.

---

## Tecnologias

| Herramienta   | Version     | Proposito                          |
|---------------|-------------|-------------------------------------|
| Python        | 3.10+       | Lenguaje principal                  |
| Scikit-Learn  | 1.9.x       | Entrenamiento y evaluacion          |
| Pandas        | 2.x         | Manipulacion de datos               |
| MLflow        | 3.x         | Registro de experimentos            |
| Pytest        | 9.x         | Pruebas automatizadas               |
| Joblib        | 1.x         | Serializacion del modelo            |

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
│   ├── prepare.py          # Carga y division del dataset
│   ├── validate_data.py    # Validacion de calidad (sin librerias externas)
│   └── train.py            # Entrenamiento y registro en MLflow
│
├── tests/
│   └── test_model.py       # 8 pruebas automatizadas con pytest
│
├── data_contract.json      # Contrato de datos para inferencia
├── requirements.txt        # Dependencias del proyecto
├── run_pipeline.py         # Script de automatizacion del pipeline
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

Este comando ejecuta automaticamente las siguientes etapas:

1. **Preparacion de datos**: carga el dataset Iris y genera `train.csv` y `test.csv` en `data/processed/`.
2. **Validacion de calidad**: verifica tipos, nulos, rangos y dominio sin librerias externas.
3. **Entrenamiento**: entrena RandomForest y registra parametros y metricas en MLflow.
4. **Pruebas automatizadas**: ejecuta 8 tests con pytest para verificar la integridad del pipeline.

Si alguna etapa falla, el pipeline se detiene automaticamente para evitar continuar con datos o resultados no validos.

### 5. Ejecucion paso a paso (opcional)

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

Abrir en el navegador: `http://localhost:5000`

Se visualiza el experimento `Iris_Pipeline_LuisPinto` con las metricas, parametros y el modelo registrado.

---

## Resultados

El modelo fue evaluado sobre el conjunto de prueba (30 registros, 20% del total) tras validacion cruzada estratificada.

| Metrica  | Valor  | Interpretacion                                         |
|----------|--------|--------------------------------------------------------|
| Accuracy | 0.9000 | El modelo clasifica correctamente el 90% de las muestras |
| F1-Score | 0.8997 | Equilibrio entre precision y recall (promedio ponderado)  |

Estos resultados son consistentes con el desempe~o esperado de RandomForest sobre Iris. La precision es adecuada para un modelo base; mejoras futuras podrian incluir optimizacion de hiperparametros o evaluacion con validacion cruzada k-fold.

---

## Contrato de datos

El archivo `data_contract.json` define las restricciones oficiales para la futura inferencia del modelo. Funciona como un acuerdo formal sobre la estructura y calidad que deben cumplir los datos de entrada.

Incluye:
- Tipos de datos esperados para cada variable
- Rangos minimos y maximos permitidos (basados en la distribucion del dataset)
- Un ejemplo de entrada valida
- Un ejemplo de entrada invalida con las razones del rechazo

---

## Pruebas automatizadas

Se implementaron 8 pruebas con pytest que verifican:

| Prueba                         | Descripcion                                    |
|--------------------------------|------------------------------------------------|
| test_archivos_procesados_existen | Verifica que train.csv y test.csv existan     |
| test_datasets_no_vacios        | Verifica que los archivos contengan registros  |
| test_columnas_correctas        | Verifica que las columnas coincidan con el estandar |
| test_sin_valores_nulos         | Verifica ausencia de valores nulos             |
| test_clases_validas            | Verifica que species contenga solo 0, 1 y 2   |
| test_modelo_existe             | Verifica que model.pkl fue generado            |
| test_modelo_carga_correctamente| Verifica que el modelo se puede cargar y tiene metodo predict |
| test_accuracy_minima           | Verifica que el accuracy sea >= 0.80           |

---

## Limitaciones

- El dataset Iris es relativamente simple (150 registros, 4 variables) y no representa la complejidad de un problema real de produccion.
- No se realizo optimizacion de hiperparametros (GridSearch o RandomSearch).
- La validacion se realizo con una unica particion train/test; una validacion cruzada k-fold proporcionaria una estimacion mas robusta.
- El modelo no fue evaluado por subgrupos (por especie) para verificar desempe~o uniforme entre clases.

---

## Autor

**Luis Pinto**
Especializacion en Ciencia de Datos
Universidad Santo Tomas
