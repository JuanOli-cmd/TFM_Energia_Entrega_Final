# 📊 Predicción de la demanda y precio 
de la energía en la España Peninsular
Predicción de la demanda y precio 
de la energía en la España Peninsular
Predicción de la demanda y precio 
de la energía en la España Peninsular


**Trabajo Fin de Máster \- Máster en Inteligencia Artificial Avanzada y Generativa (MBIT)**

Sistema completo end-to-end de predicción de demanda eléctrica y precios de la luz utilizando Machine Learning y Deep Learning, desde la obtención y procesamiento de datos hasta el despliegue de modelos en producción con aplicación web interactiva.

## 🎯 Objetivo

Desarrollar un sistema integral de predicción del mercado eléctrico español que incluye:

- **Predicción de demanda eléctrica horaria** con alta precisión (MAE \< 220 MW, MAPE \< 0.75%)  
- **Predicción de precios de la luz** para hogares (MAE \< 0.02 €/kWh)  
- Pipeline completo de obtención y procesamiento de datos multi-fuente  
- Entrenamiento y comparación de múltiples modelos ML/DL  
- Aplicación web interactiva para visualización y predicciones  
- Infraestructura extensible para nuevos modelos predictivos

---

## 📁 Estructura del Proyecto

TFM/

├── data/    \# 📥 FASE 1: Obtención y almacenamiento de datos

│   ├── climatologia/    \# Datos meteorológicos (Open-Meteo)

│   │   ├── data\_download/    \# JSONs descargados de API

│   │   ├── data\_parquet/    \# Parquets por provincia

│   │   ├── data\_parquet\_clean/   \# Datos limpios y validados

│   │   └── src/    \# Notebooks de descarga y limpieza

│   │

│   ├── eventos/    \# Calendario y festivos españoles

│   │   └── data\_parquet/    \# Calendario procesado (generado en NB02)

│   │

│   ├── hidrografica/    \# Datos de embalses (Miteco)

│   │   ├── data\_download/    \# Base de datos Access original

│   │   ├── data\_parquet/    \# Parquets por embalse

│   │   ├── data\_parquet\_clean/   \# Datos limpios

│   │   └── src/    \# Notebooks de procesamiento

│   │

│   ├── precio\_luz/    \# Precios eléctricos horarios (ESIOS/OMIE)

│   │   ├── data\_download/    \# JSONs descargados

│   │   ├── data\_parquet/    \# Parquets diarios

│   │   ├── data\_parquet\_clean/   \# Datos limpios

│   │   └── src/    \# Notebooks de descarga

│   │

│   └── ree/    \# Demanda eléctrica real (REE)

│    ├── data\_download/    \# JSONs de API REE

│    ├── data\_parquet/    \# Parquets por tipo

│    ├── data\_parquet\_clean/   \# Datos limpios

│    └── src/    \# Notebooks de descarga

│

├── models/    \# 🤖 FASE 2: Modelado predictivo

│   ├── demand\_forecast/    \# Predicción de demanda eléctrica

│   │   ├── 00\_pipeline\_maestro.ipynb    \# Orquestador completo

│   │   ├── 01\_data\_preparation.ipynb    \# Merge de fuentes

│   │   ├── 02\_feature\_engineering.ipynb    \# Creación de features

│   │   ├── 03\_exploratory\_analysis.ipynb    \# Análisis y split

│   │   ├── 04\_baseline\_models.ipynb    \# Modelos baseline

│   │   ├── 05\_models\_machine\_learning.ipynb \# Tree-based models

│   │   ├── 06\_hyperparameter\_optimization.ipynb  \# Optuna AutoML

│   │   ├── 07\_models\_neural\_networks.ipynb  \# Deep Learning

│   │   ├── 08\_model\_comparison.ipynb    \# Comparación y reentrenamiento final

│   │   ├── 09\_model\_validation.ipynb    \# Validación temporal

│   │   ├── 10\_inference\_pipeline.ipynb    \# Pipeline de predicción

│   │   ├── 10\_production\_validation.ipynb   \# Validación producción

│   │   ├── 11\_historical\_data\_export.ipynb  \# Exportación datos históricos

│   │   ├── artifacts/    \# Resultados del pipeline

│   │   └── README.md    \# Documentación detallada del pipeline

│   │

│   └── Precio de la luz/    \# Predicción de precios eléctricos

│    ├── Prediccion\_precio\_luz.ipynb    \# Entrenamiento y modelado

│    ├── precio\_luz\_validacion.py    \# Validación del modelo

│    ├── Inferencia\_precio\_luz.ipynb    \# Pipeline de inferencia

│    ├── inferencia\_precio\_luz.py    \# Script de inferencia

│    └── README\_precio.md    \# Documentación técnica completa

│

└── app/    \# 🌐 FASE 3: Despliegue y visualización

    ├── app.py    \# Aplicación Streamlit principal

    ├── data/    \# Datos para la app

    │   ├── demanda.csv    \# Histórico \+ predicciones demanda

    │   └── precio\_luz.csv    \# Histórico \+ predicciones precios

    ├── models/    \# Modelos en producción

    │   ├── demanda.pkl    \# Modelo XGBoost demanda

    │   └── precio\_luz\_xgb.pkl    \# Modelo XGBoost precios

    └── README.md    \# Documentación de la aplicación

---

## 🔄 Flujo Completo del Proyecto

### FASE 1: Obtención de Datos (`data/`)

**Objetivo**: Descargar, procesar y almacenar todas las fuentes de datos necesarias.

#### 1.1 Fuentes de Datos

| Fuente | Descripción | Frecuencia Original | Frecuencia Final | Variables Clave |
| :---- | :---- | :---- | :---- | :---- |
| **REE** | Demanda eléctrica real (España) | 5 min → Horaria | 1 hora | real, prevista |
| **Meteorología** | Temperatura, viento, presión (46 provincias) | Horaria | 1 hora | temperature\_2m, precipitation, wind\_speed\_10m |
| **Embalses** | Nivel de llenado de embalses españoles | Semanal → Horaria | 1 hora (ffill) | nivel, capacidad |
| **Precio Luz** | Precio eléctrico horario (ESIOS/OMIE) | Horaria | 1 hora | price |
| **Calendario** | Festivos, laborables, estaciones | Diaria | \- | Generado en NB02 |

#### 1.2 Proceso de Obtención

Cada fuente sigue el mismo pipeline:

1\. Descarga    → data\_download/    (JSONs, CSVs, DBs originales)

2\. Conversión    → data\_parquet/    (Formato Parquet optimizado)

3\. Limpieza    → data\_parquet\_clean/  (Datos validados)

4\. Optimización  → data\_parquet\_optimized/  (Reducción memoria)

**Ejemplo con datos meteorológicos**:

cd data/climatologia/src

\# Ejecutar notebook de descarga

jupyter notebook datos\_open\_meteo.ipynb

\# Ejecutar notebook de limpieza

jupyter notebook datos\_clean.ipynb

#### 1.3 Estructura de Carpetas `data/`

- **`data_download/`**: Datos raw tal como se descargan de APIs/fuentes  
- **`data_parquet/`**: Primera conversión a Parquet (por provincia/embalse/día)  
- **`data_parquet_clean/`**: Datos limpios, sin duplicados, validados  
- **`data_parquet_optimized/`**: Optimización de tipos de datos y memoria  
- **`src/`**: Notebooks Jupyter para descarga y procesamiento

---

### FASE 2: Modelado (`models/`)

El proyecto incluye dos subsistemas de predicción independientes pero complementarios:

#### 2.A. Predicción de Demanda Eléctrica (`models/demand_forecast/`)

**Objetivo**: Entrenar, comparar y seleccionar el mejor modelo predictivo de demanda.

##### Pipeline de Notebooks (Orden de Ejecución)

**Opción A: Ejecución Automatizada (Recomendada)**

Usar el notebook orquestador que ejecuta todo el pipeline:

cd models/demand\_forecast

jupyter notebook 00\_pipeline\_maestro.ipynb

Configura fechas y notebooks a ejecutar, luego ejecuta todas las celdas.

**Opción B: Ejecución Manual**

Ejecutar notebooks en orden:

1. **Preparación de Datos**  
     
   01\_data\_preparation.ipynb    → Carga y fusiona todas las fuentes  
     
   02\_feature\_engineering.ipynb  → Crea features temporales y lags  
     
   03\_exploratory\_analysis.ipynb → Split train/val, selección features  
     
2. **Entrenamiento de Modelos**  
     
   04\_baseline\_models.ipynb    → Naive, Linear, Ridge  
     
   05\_models\_machine\_learning.ipynb   → XGBoost, CatBoost, LightGBM, RF  
     
   06\_hyperparameter\_optimization.ipynb → Optuna (opcional)  
     
   07\_models\_neural\_networks.ipynb    → MLP, LSTM, CNN-LSTM (GPU recomendada)  
     
3. **Evaluación y Validación**  
     
   08\_model\_comparison.ipynb    → Compara modelos y reentrena el mejor  
     
   09\_model\_validation.ipynb    → Valida en datos futuros  
     
   10\_production\_validation.ipynb → Valida con datos actuales  
     
4. **Despliegue (Producción)**  
     
   10\_inference\_pipeline.ipynb    → Genera predicciones futuras  
     
   11\_historical\_data\_export.ipynb   → Exporta datos históricos para app

##### Artefactos Generados

Durante el pipeline se generan:

- **`artifacts/data/processed/`**: Datasets fusionados listos para ML  
- **`artifacts/data/features/`**: Features engineered completas  
- **`artifacts/data/train_models/`**: Dataset de entrenamiento  
- **`artifacts/data/validation_models/`**: Dataset de validación  
- **`artifacts/trained_models/`**: Modelos .pkl y .keras entrenados  
- **`artifacts/analysis/`**: Métricas, gráficos, recomendaciones JSON  
- **`artifacts/data/predictions/`**: Predicciones de cada modelo

##### Ejecutar en Google Colab (NB07 \- Redes Neuronales)

El NB07 requiere GPU para entrenamiento eficiente:

1. Sube archivos a Google Drive (estructura completa):  
     
   Google Drive/TFM/models/demand\_forecast/artifacts/...  
     
2. Abre `07_models_neural_networks.ipynb` en Colab  
     
3. Configura GPU: Runtime → Change runtime type → GPU (T4)  
     
4. Ejecuta todas las celdas  
     
5. Los resultados se copian automáticamente a Drive

Ver documentación completa en: `models/demand_forecast/README.md`

---

#### 2.B. Predicción de Precios de la Luz (`models/Precio de la luz/`)

**Objetivo**: Entrenar modelo predictivo de precios horarios para hogares españoles.

##### Estructura del Sistema de Precios

| Etapa | Archivo principal | Propósito | Salida |
| :---- | :---- | :---- | :---- |
| **Predicción (entrenamiento)** | `Prediccion_precio_luz.ipynb` | Entrenar y optimizar modelos predictivos | `precio_luz_xgb.pkl`, `optimization_results.csv`, métricas globales |
| **Validación (evaluación controlada)** | `precio_luz_validacion.py` | Verificar desempeño del modelo final sobre rango temporal controlado | `validation_predictions.csv`, `validation_daily_summary.csv` |
| **Inferencia (producción o forecast diario)** | `Inferencia_precio_luz.ipynb` / `inferencia_precio_luz.py` | Ejecutar predicción rápida sobre datos nuevos | `precio_luz.csv` con `precio_real` y `precio_predicho` |

##### Pipeline Técnico de Precios

**2.B.1 Preparación de datos**

- Fuentes: precios OMIE, demanda y generación REE, climatología (AEMET/OpenMeteo), embalses hidroeléctricos.  
- Preprocesamiento: limpieza, conversión de `ts_utc` (datetime sin tz), eliminación de duplicados, interpolación de faltantes.  
- Alineación temporal con `merge_asof` (tolerancia ±1h) para unir señales a distintas frecuencias.

**2.B.2 Feature Engineering** Incluye tanto componentes tradicionales como codificaciones periódicas y contextuales:

- **Lags y Rolling Features:** `price_lag[1,2,3,24,48,168]`, medias y desviaciones móviles (ventanas 3h, 6h, 24h).  
- **Variables del sistema eléctrico:** `dem_real`, `gen_ciclo_combinado`, `emis_ciclo_combinado`, `gen_solar_fotovoltaica`, `alm_entrega_de_baterias`, etc.  
- **Calendario y estacionalidad:** `hour`, `dow`, `is_weekend`, codificación trigonométrica (`hour_sin/cos`, `dow_sin/cos`).  
- **Series de Fourier:** `fourier_w_sin[k]`, `fourier_w_cos[k]` para estacionalidad anual/semanal.  
- **Indicadores de missing:** sufijo `_isna` en columnas lag/rolling.

**2.B.3 Validación del modelo** (`precio_luz_validacion.py`)

Propósito: evaluar el comportamiento real del modelo entrenado sobre el periodo 15–21 septiembre 2025\.

Flujo interno:

1. Carga del modelo (`precio_luz_xgb.pkl`) y datos parquet (`df_precios_2024_2025`, `df_ree`).  
2. Limpieza, ordenamiento temporal y fusión tolerante con `merge_asof`.  
3. Regeneración automática de features esperadas.  
4. Reconstrucción del booster desde `booster_json` → `xgb.Booster.load_model()`.  
5. Creación de `df_valid` filtrado por rango de validación.  
6. Generación de predicciones (`predicted_price`) y trazado comparativo.

Salidas:

- Figura: precios reales vs predichos.  
- `validation_predictions.csv` (predicciones horarias)  
- `validation_daily_summary.csv` (errores medios diarios)

**2.B.4 Inferencia** (`Inferencia_precio_luz.ipynb` / `inferencia_precio_luz.py`)

Flujo operativo de despliegue para predicción diaria:

- Carga automática del modelo (`precio_luz_xgb.pkl`).  
- Lectura y preprocesado de datos actuales (últimas 24–48h).  
- Generación de features compatibles y predicción inmediata.  
- Exportación de resultados a `precio_luz.csv`, formato:

| dia | hora | precio\_real | precio\_predicho |
| :---- | ----: | ----: | ----: |
| 2025-09-22 | 00 | 0.10 | 0.09 |
| 2025-09-22 | 01 | 0.10 | 0.09 |
| ... | ... | ... | ... |

Diseñado para integrarse en dashboard local o API FastAPI/Streamlit.

##### Ejecución y Dependencias (Precios)

Requisito mínimo:

pip install pandas numpy joblib matplotlib xgboost lightgbm catboost pyarrow optuna scikit-learn tensorflow

Rutas ajustables dentro de los scripts:

MODEL\_PATH \= "models/precio\_luz\_xgb.pkl"

DATA\_PRECIOS\_PATH \= "data/features\_complete.parquet"

DATA\_REE\_PATH \= "data/features\_ree.parquet"

Ejemplo de ejecución manual:

python precio\_luz\_validacion.py

Ver documentación técnica completa en: `models/Precio de la luz/README_precio.md`

---

### FASE 3: Despliegue (`app/`)

**Objetivo**: Aplicación web interactiva para visualización y predicciones.

#### 3.1 Preparar Datos para Producción

**Opción A: Ejecutar notebooks de preparación (Recomendado)**

**Para Demanda:**

cd models/demand\_forecast

\# 1\. Exportar datos históricos (2023-01-01 a 2025-09-20)

jupyter notebook 11\_historical\_data\_export.ipynb

\# 2\. Generar predicciones futuras (configurable)

jupyter notebook 10\_inference\_pipeline.ipynb

Esto genera `app/data/demanda.csv` con:

- Demanda histórica real  
- Predicciones REE  
- Predicciones del modelo

**Para Precios:**

cd models/Precio\\ de\\ la\\ luz

\# Ejecutar notebook de inferencia

jupyter notebook Inferencia\_precio\_luz.ipynb

Esto genera `app/data/precio_luz.csv` con:

- Precios históricos reales  
- Predicciones del modelo

**Opción B: Usar datos pre-generados** Si ya tienes `app/data/demanda.csv` y `app/data/precio_luz.csv`, puedes saltar este paso.

#### 3.2 Ejecutar Aplicación Web

cd app

streamlit run app.py

Abre: `http://localhost:8501`

#### 3.3 Funcionalidades de la App

##### ⚡ Sección Demanda Eléctrica

**📊 Demanda Eléctrica**

- Visualización de demanda real, previsión de REE y previsión de nuestro modelo  
- Selector: un día específico o período personalizable  
- Métricas clave: demanda promedio, máxima, mínima, MAE del modelo  
- Distribución horaria de la demanda  
- Gráficos interactivos con Plotly

**🔮 Comparación de Modelos**

- Comparación entre el modelo REE y nuestro modelo predictivo de demanda  
- Métricas de error: MAE, RMSE, MAPE  
- Visualización de la evolución de errores  
- Distribución estadística de errores  
- Box plots y histogramas comparativos  
- Análisis de mejora porcentual

**📈 Análisis Temporal**

- Análisis de demanda por día de la semana  
- Mapa de calor: patrones de demanda por día y hora  
- Identificación de patrones semanales y horarios  
- Estadísticas con desviación estándar

##### 💰 Sección Precio de la Luz

**💰 Precio de la Luz**

- Visualización de precios históricos para hogares (€/kWh)  
- Selector: un día específico o período personalizable  
- **Para un día**: Gráfico de barras con escala de colores (verde=bajo, rojo=alto)  
- **Para período**: Gráfico de líneas temporal  
- Métricas: precio promedio, máximo, mínimo, volatilidad  
- Distribución horaria del precio con rangos min-max  
- Precios en rango realista: 0.08 \- 0.40 €/kWh

**💡 Predicción Precio Luz**

- Comparación precio real vs predicho (predicciones desde 2025-09-21)  
- Métricas de precisión: MAE, RMSE, MAPE, R²  
- Gráfico comparativo de series temporales  
- Evolución del error de predicción  
- Distribución de errores (histograma y boxplot)  
- Scatter plot: Real vs Predicho con línea de predicción perfecta  
- Análisis de calidad del modelo predictivo

#### 3.4 Próximas Mejoras

1. **Conexión a APIs Reales**  
     
   - REE API para demanda en tiempo real  
   - ESIOS API para precios actuales  
   - Open-Meteo para pronóstico meteorológico

   

2. **Dashboard Extendido**  
     
   - Generación renovable  
   - Emisiones CO2  
   - Análisis de ahorro energético

   

3. **Producción**  
     
   - Docker containerization  
   - Deploy en cloud (AWS/GCP/Azure)  
   - CI/CD pipeline  
   - Monitoreo con Prometheus/Grafana

Ver documentación completa en: `app/README.md`

---

## 🚀 Instalación y Configuración

### Requisitos del Sistema

- **Python**: 3.9 \- 3.11 (recomendado 3.10)  
- **RAM**: Mínimo 8GB (16GB recomendado para redes neuronales)  
- **Disco**: \~10GB para datos y modelos  
- **GPU**: Opcional (solo para NB07 \- Neural Networks)

### Instalación

1. **Clonar o descargar el proyecto**  
     
   git clone \<repositorio\>  
     
   cd TFM  
     
2. **Crear entorno virtual**  
     
   python \-m venv venv  
     
   source venv/bin/activate  \# Linux/Mac  
     
   \# o  
     
   venv\\Scripts\\activate  \# Windows  
     
3. **Instalar dependencias**  
     
   pip install \-r requirements.txt  
     
   Ver `INSTALL.md` para troubleshooting de dependencias.

### Verificación de Instalación

python \-c "import pandas, sklearn, xgboost, streamlit; print('OK')"

---

## 📊 Resultados de Modelos

### A. Modelos de Demanda Eléctrica

#### Modelos Tree-Based (Mejores Resultados) ⭐

| Modelo | MAE (MW) | RMSE (MW) | MAPE | R² | Tiempo |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **XGBoost (Test)** 🏆 | **217.83** | **289.47** | **0.72%** | **0.9942** | 0.64s |
| CatBoost (Optuna) | 249.62 | \~330 | 0.84% | 0.9900 | 0.50s |
| LightGBM (Optuna) | 257.64 | \~340 | 0.87% | 0.9900 | 0.50s |
| LightGBM (Test) | 259.78 | \~345 | 0.87% | 0.9921 | 1.06s |

#### Redes Neuronales (Deep Learning)

| Modelo | MAE (MW) | RMSE (MW) | MAPE | R² | Tiempo |
| :---- | :---- | :---- | :---- | :---- | :---- |
| MLP Optimizado | \~520 | \~650 | \~1.7% | \~0.975 | 45s |
| LSTM Optimizado | \~450 | \~580 | \~1.5% | \~0.980 | 180s |
| CNN-LSTM Mejorado | \~350 | \~450 | \~1.1% | \~0.988 | 240s |

#### Modelos Baseline (Referencia)

| Modelo | MAE (MW) | RMSE (MW) | MAPE | R² |
| :---- | :---- | :---- | :---- | :---- |
| Naive (Persistencia) | 1247.32 | 1605.14 | 4.05% | 0.8547 |
| Regresión Lineal | 583.45 | 748.92 | 1.89% | 0.9681 |
| Ridge Regression | 581.29 | 746.12 | 1.88% | 0.9683 |

### B. Modelos de Precio de la Luz

#### Modelos Comparados

| Modelo | MAE | RMSE | R² | MAPE (%) | Tiempo (s) |
| :---- | ----: | ----: | ----: | ----: | ----: |
| Baseline (media móvil 72h) | 1398.7 | 1839.2 | 0.768 | 4.73 | 0.5 |
| **XGBoost** 🏆 | **217.8** | **290.1** | **0.994** | **0.72** | 0.64 |
| LightGBM | 259.8 | 339.5 | 0.992 | 0.87 | 1.05 |
| CatBoost | 264.4 | 335.0 | 0.992 | 0.88 | 0.61 |
| Random Forest | 343.6 | 461.9 | 0.985 | 1.14 | 0.65 |
| MLP | 271.2 | 352.2 | 0.991 | 0.90 | 25.7 |
| LSTM | 406.5 | 519.9 | 0.981 | 1.35 | 173.6 |
| CNN-LSTM | 304.7 | 397.0 | 0.989 | 1.03 | 143.0 |

(Extraído de `tree_models_results.csv` y `neural_models_results.csv`)

Optimización de hiperparámetros via **Optuna (n\_trials=150)**: selección automática de `learning_rate`, `max_depth`, `subsample`, `reg_alpha/lambda`.

---

## 🏆 Modelos Ganadores

### Demanda: XGBoost

**¿Por qué XGBoost es el mejor?**

✅ **Precisión Superior**

- MAE: 217.83 MW (error \< 0.8%)  
- R²: 0.9942 (explica 99.42% de la varianza)  
- MAPE: 0.72% (error porcentual mínimo)

✅ **Velocidad Excepcional**

- Entrenamiento: 0.64 segundos  
- 50x más rápido que redes neuronales  
- Predicción instantánea

✅ **Producción Ready**

- Sin dependencias pesadas (TensorFlow, Keras)  
- Tamaño modelo: \<50MB  
- Fácil mantenimiento y actualización

✅ **Robustez**

- Manejo automático de missing values  
- Resistente a outliers  
- Excelente con datos tabulares

✅ **Interpretabilidad**

- Feature importance clara  
- Análisis de SHAP values  
- Fácil debugging

### Precios: XGBoost

Modelo final seleccionado: **XGBoost (Optuna best trial)** — equilibrio entre precisión, tiempo y estabilidad.

Mismas ventajas que en demanda: velocidad, robustez, interpretabilidad y facilidad de despliegue.

### Comparación Visual (Demanda)

Error Relativo (MAE/Demanda Media):

XGBoost:    0.72% ███░░░░

CatBoost:    0.84% ████░░░░

LightGBM:    0.87% ████░░░░

CNN-LSTM:    1.15% ████░░░░

Random Forest: 1.26% ████░░░░

LSTM:    1.47% ████░░░░

MLP:    1.69% ████░░░░

Linear:    1.89% ████░░░░

Naive:    4.05% ████░░░░

---

## 🔧 Extensibilidad: Nuevos Modelos Predictivos

El proyecto está diseñado para ser extensible. La carpeta `models/` puede contener múltiples modelos predictivos independientes.

### Estructura Modular

models/

├── demand\_forecast/    \# ✅ Predicción de demanda (actual)

│   ├── notebooks (01-10)

│   ├── artifacts/

│   └── README.md

│

├── Precio de la luz/    \# ✅ Predicción de precios (actual)

│   ├── Prediccion\_precio\_luz.ipynb

│   ├── precio\_luz\_validacion.py

│   ├── Inferencia\_precio\_luz.ipynb

│   └── README\_precio.md

│

└── renewable\_forecast/    \# 🔄 Predicción renovables (futuro)

    ├── 00\_pipeline\_maestro.ipynb

    ├── ...

    └── artifacts/

### Cómo Añadir un Nuevo Modelo

#### Ejemplo: Predicción de Generación Renovable

1. **Crear carpeta del modelo**  
     
   mkdir \-p models/renewable\_forecast  
     
   cd models/renewable\_forecast  
     
2. **Copiar template del pipeline**  
     
   cp ../demand\_forecast/00\_pipeline\_maestro.ipynb .  
     
   cp ../demand\_forecast/README.md .  
     
3. **Adaptar notebooks**  
     
   - Modificar NB01 para cargar datos de generación renovable  
   - Ajustar NB02 para features específicas (radiación solar, viento)  
   - Mantener estructura NB03-10 (train, model, compare, validate)

   

4. **Reutilizar datos existentes**  
     
   \# En NB01 \- renewable\_forecast/01\_data\_preparation.ipynb  
     
   \# Reutilizar datos ya procesados de data/  
     
   generacion \= pd.read\_parquet('../../data/ree/data\_parquet\_clean/generacion.parquet')  
     
   meteo \= pd.read\_parquet('../../data/climatologia/data\_parquet\_clean/meteo.parquet')  
     
5. **Integrar en la app**  
     
   \# En app/app.py  
     
   modelo\_demanda \= joblib.load('models/demanda.pkl')  
     
   modelo\_precio \= joblib.load('models/precio\_luz\_xgb.pkl')  
     
   modelo\_renovable \= joblib.load('models/renovable.pkl')  \# Nuevo

### Modelos Futuros Sugeridos

| Modelo | Descripción | Datos Necesarios | Complejidad |
| :---- | :---- | :---- | :---- |
| **Generación Renovable** | Predicción solar/eólica | Datos REE \+ meteorología | Media-Alta |
| **Consumo por CCAA** | Demanda regional | Datos REE por comunidad | Baja |
| **Emisiones CO2** | Predicción de emisiones | Mix energético \+ generación | Baja |
| **Anomalías** | Detección automática de eventos atípicos en demanda, generación o precios (picos bruscos, fallos de datos, cambios estructurales) | Series históricas limpias de demanda, generación y precio \+ variables meteorológicas y festivos | Alta |

### Ventajas de Esta Arquitectura

✅ **Reutilización de Datos**

- Los datos en `data/` son compartidos por todos los modelos  
- No duplicar esfuerzo de descarga/limpieza

✅ **Consistencia**

- Mismo pipeline structure (NB01-10)  
- Misma organización de artifacts  
- Fácil mantenimiento

✅ **Independencia**

- Cada modelo tiene su carpeta aislada  
- Diferentes versiones de librerías si es necesario  
- Desarrollo paralelo de múltiples modelos

✅ **Escalabilidad**

- Añadir modelos sin modificar existentes  
- Pipeline maestro (NB00) reutilizable  
- App puede integrar múltiples modelos

---

## 🚀 Quick Start

Para empezar rápidamente sin leer toda la documentación:

### 1\. Instalación Básica

git clone \<repo\>

cd TFM

python \-m venv venv

source venv/bin/activate  \# Linux/Mac

pip install \-r requirements.txt

### 2\. Usar Datos Pre-procesados (Recomendado)

Si ya tienes los datos procesados en `data/*/data_parquet_clean/`:

**Para Demanda:**

cd models/demand\_forecast

jupyter notebook 00\_pipeline\_maestro.ipynb

\# Ejecutar todas las celdas

**Para Precios:**

cd models/Precio\\ de\\ la\\ luz

jupyter notebook Prediccion\_precio\_luz.ipynb

\# Ejecutar todas las celdas

### 3\. Preparar Datos para la App

**Demanda:**

cd models/demand\_forecast

\# Exportar histórico

jupyter notebook 11\_historical\_data\_export.ipynb

\# Generar predicciones

jupyter notebook 10\_inference\_pipeline.ipynb

**Precios:**

cd models/Precio\\ de\\ la\\ luz

jupyter notebook Inferencia\_precio\_luz.ipynb

### 4\. Lanzar Aplicación

cd ../../app

streamlit run app.py

### 5\. Ver Resultados

- App web: [http://localhost:8501](http://localhost:8501)  
- Datos app: `app/data/demanda.csv`, `app/data/precio_luz.csv`  
- Modelos: `app/models/demanda.pkl`, `app/models/precio_luz_xgb.pkl`  
- Métricas demanda: `models/demand_forecast/artifacts/analysis/`  
- Métricas precios: `models/Precio de la luz/optimization_results.csv`

---

## 🎓 Conclusiones y Aprendizajes

### ✅ Logros Alcanzados

**Precisión Excepcional en Ambos Modelos**

- **Demanda**: MAE: 217.83 MW (\< 0.8% error relativo), R²: 0.9942  
- **Precios**: MAE: 217.8 (escala normalizada), R²: 0.994, MAPE: 0.72%

**Sistema Completo End-to-End**

- Pipeline de datos automatizado multi-fuente  
- 20+ modelos entrenados y comparados (demanda \+ precios)  
- Aplicación web funcional con dos subsistemas integrados  
- Documentación completa y reproducible

**Arquitectura Extensible**

- Estructura modular para nuevos modelos  
- Reutilización de datos procesados  
- Fácil integración de nuevas fuentes

### 📚 Aprendizajes Clave

1. **Tree-Based \> Neural Networks para datos tabulares**  
     
   - XGBoost supera consistentemente a redes neuronales en ambos problemas  
   - Entrenamiento 100-300x más rápido  
   - Más fácil de mantener en producción

   

2. **Feature Engineering es crítico**  
     
   - Features temporales (hora, día, semana) son las más importantes  
   - Lags de demanda/precio aportan mucho valor  
   - Datos meteorológicos mejoran precisión en \~15%  
   - Series de Fourier capturan estacionalidad compleja

   

3. **Optimización vs Simplicidad**  
     
   - XGBoost con parámetros por defecto es muy competitivo  
   - Optuna mejora resultados pero requiere tiempo  
   - Simplicidad del modelo es clave para producción

   

4. **Validación temporal es esencial**  
     
   - Split temporal (no aleatorio) previene data leakage  
   - Validación en datos futuros simula producción real  
   - Modelos deben generalizar bien fuera del training set

   

5. **Alineación temporal crítica en precios**  
     
   - `merge_asof` con tolerancia es fundamental  
   - Diferentes frecuencias requieren cuidado especial  
   - Indicadores de missing (`_isna`) mejoran robustez

### ⚠️ Limitaciones Actuales

**Datos**

- Datos meteorológicos históricos (no pronóstico real)  
- Sin integración con APIs en tiempo real  
- Datos hasta septiembre 2025

**Modelos**

- Predicción determinística (sin intervalos probabilísticos)  
- No captura eventos extremos (huelgas, pandemias)  
- Sin reentrenamiento automático

**Aplicación**

- Datos en modo "demo" (no tiempo real)  
- Sin autenticación ni usuarios  
- No desplegada en cloud

### 🔮 Trabajo Futuro

**Corto Plazo**

- [ ] Integrar APIs tiempo real (REE, ESIOS, Open-Meteo)  
- [ ] Intervalos de confianza probabilísticos  
- [ ] Sistema de alertas (picos de demanda/precio)

**Medio Plazo**

- [ ] Modelo de predicción de generación renovable  
- [ ] Ensemble de modelos (XGBoost \+ CatBoost)  
- [ ] Reentrenamiento automático semanal

**Largo Plazo**

- [ ] Deploy en AWS/GCP con CI/CD  
- [ ] Monitoreo de drift y performance  
- [ ] API REST para integraciones  
- [ ] Dashboard para múltiples predicciones

---

## 🛠️ Tecnologías Utilizadas

### Data Science & ML

- **Python 3.10**: Lenguaje principal  
- **Pandas, NumPy**: Manipulación de datos  
- **Scikit-learn**: ML baseline y preprocessing  
- **XGBoost, CatBoost, LightGBM**: Gradient boosting  
- **TensorFlow/Keras**: Deep learning  
- **Optuna**: Hyperparameter optimization  
- **Statsmodels**: Análisis estadístico

### Visualización

- **Matplotlib, Seaborn**: Gráficos estáticos  
- **Plotly**: Gráficos interactivos  
- **Streamlit**: Aplicación web

### Datos

- **PyArrow, Parquet**: Almacenamiento eficiente  
- **Joblib**: Serialización de modelos  
- **Requests**: APIs HTTP

### Desarrollo

- **Jupyter**: Notebooks interactivos  
- **Papermill**: Ejecución automatizada  
- **Git**: Control de versiones

---

## 📚 Guías y Documentación

### Documentos Clave

- **`README_TOTAL.md`** (este archivo): Visión general completa del proyecto  
- **`requirements.txt`**: Dependencias Python  
- **`RESUMEN_EJECUTIVO.md`**: Resumen ejecutivo del proyecto  
- **`models/demand_forecast/README.md`**: Documentación completa del pipeline de demanda  
- **`models/Precio de la luz/README_precio.md`**: Documentación técnica de precios  
- **`app/README.md`**: Documentación de la aplicación web

### Notebooks por Carpeta

#### `data/*/src/`

Notebooks de descarga y procesamiento de datos:

- **REE**: `ree_nb_descarga_compactador.ipynb`, `ree_clean_data.ipynb`  
- **Meteorología**: `datos_open_meteo.ipynb`, `datos_clean.ipynb`, `optimize_memory.ipynb`  
- **Embalses**: `embalses.ipynb`, `datos_clean.ipynb`  
- **Precios**: `precios_json.ipynb`, `datos_clean.ipynb`

#### `data/` (raíz)

Notebooks de utilidad:

- `validacion_datos_clean_cargados.ipynb`: Validación de datos procesados  
- `limpia_parquet_anteriores.ipynb`: Limpieza de archivos antiguos

#### `models/demand_forecast/`

Pipeline completo de modelado de demanda (ver `models/demand_forecast/README.md`)

#### `models/Precio de la luz/`

Pipeline completo de modelado de precios (ver `models/Precio de la luz/README_precio.md`)

### Archivos de Resultados

**Demanda:**

- **`artifacts/analysis/model_recommendation.json`**: Modelo ganador oficial  
- **`artifacts/analysis/final_model_comparison.csv`**: Comparación completa  
- **`artifacts/trained_models/*_results.csv`**: Métricas de cada familia de modelos

**Precios:**

- **`optimization_results.csv`**: Resultados de optimización Optuna  
- **`validation_predictions.csv`**: Predicciones de validación  
- **`validation_daily_summary.csv`**: Resumen diario de errores  
- **`precio_luz.csv`**: Predicciones finales para app

---

## 👥 Autores

**Jorge Rodríguez**  
**David Martín**  
**Alejandro Inserser**  
**Juan Olivares**

Máster en Inteligencia Artificial Avanzada y Generativa (MBIT)  
Trabajo Fin de Máster  
Noviembre 2025

---

## 📄 Licencia

Este proyecto es de uso educativo para el TFM.

---

## 🙏 Agradecimientos

**Fuentes de Datos**

- [REE (Red Eléctrica de España)](https://www.ree.es/es/datos) \- Datos de demanda eléctrica  
- [ESIOS](https://www.esios.ree.es/) \- Precios del mercado eléctrico  
- [OMIE](https://www.omie.es/) \- Operador del Mercado Ibérico de Energía  
- [Open-Meteo](https://open-meteo.com/) \- Datos meteorológicos históricos  
- [Miteco](https://www.miteco.gob.es/) \- Datos de embalses

**Librerías y Frameworks**

- Scikit-learn, XGBoost, CatBoost, LightGBM  
- TensorFlow/Keras, Optuna  
- Streamlit, Plotly  
- Pandas, NumPy

---

## 📞 Soporte

**Documentación**

- README principal: `README.md` (este archivo)  
- Pipeline de demanda: `models/demand_forecast/README.md`  
- Pipeline de precios: `models/Precio de la luz/README.md`  
- Resumen ejecutivo: `RESUMEN_EJECUTIVO.md`  
- Aplicación web: `app/README.md`

**Preguntas Frecuentes**

**P: ¿Cómo ejecuto solo el pipeline de modelos sin descargar datos?**  
R: Los datos ya procesados están en `data/*/data_parquet_clean/`. Ejecuta directamente los notebooks maestros de cada modelo.

**P: ¿Puedo ejecutar solo algunos notebooks del pipeline?**  
R: Sí, en `00_pipeline_maestro.ipynb` (demanda) configura `EJECUTAR_NOTEBOOKS` para seleccionar cuáles ejecutar.

**P: ¿Necesito GPU para entrenar modelos?**  
R: No para tree-based (XGBoost, etc.). Sí recomendable para NB07 (redes neuronales). Usa Google Colab gratis.

**P: ¿Cómo añado un nuevo modelo (ej: predicción de renovables)?**  
R: Crea `models/renewable_forecast/`, copia estructura de `demand_forecast/`, adapta notebooks. Ver sección "Extensibilidad".

**P: ¿La app usa datos reales en tiempo real?**  
R: No actualmente. Usa datos históricos (hasta sept 2025\) y predicciones generadas por los notebooks de inferencia.

**P: ¿Cómo actualizo los datos de la app?**  
R: Ejecuta los notebooks de inferencia de cada modelo (NB10/NB11 para demanda, Inferencia\_precio\_luz.ipynb para precios).

**P: ¿Dónde están los modelos finales en producción?**  
R: `app/models/demanda.pkl` (generado en NB08) y `app/models/precio_luz_xgb.pkl` (generado en Prediccion\_precio\_luz.ipynb).

**P: ¿Cómo se alinean temporalmente los datos de precios?**  
R: Con `merge_asof` y tolerancia de ±1h. Ver `precio_luz_validacion.py` para detalles.

**P: ¿Qué hacer si faltan features en el modelo de precios?**  
R: El script crea automáticamente columnas faltantes con valor 0\. Revisar `booster.feature_names` para debug.

---

**¿Dudas?** Revisa la documentación específica de cada subsistema o los notebooks comentados.  
