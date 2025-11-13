# Modelo de Predicción de Demanda Eléctrica

Este directorio contiene el desarrollo completo de un modelo de Machine Learning para predecir la demanda eléctrica en España con frecuencia horaria.

## 📁 Estructura del Proyecto

demand\_forecast/

├── 00\_pipeline\_maestro.ipynb          \# Orquestador completo del pipeline

├── 01\_data\_preparation.ipynb          \# Preparación y limpieza de datos

├── 02\_feature\_engineering.ipynb       \# Creación de features

├── 03\_exploratory\_analysis.ipynb      \# Análisis exploratorio de datos

├── 04\_baseline\_models.ipynb           \# Modelos baseline de referencia

├── 05\_models\_machine\_learning.ipynb   \# Modelos basados en árboles

├── 06\_hyperparameter\_optimization.ipynb \# Optimización automática con Optuna

├── 07\_models\_neural\_networks.ipynb    \# Redes neuronales

├── 08\_model\_comparison.ipynb          \# Comparación de modelos

├── 09\_model\_validation.ipynb           \# Validación temporal

├── 10\_inference\_pipeline.ipynb        \# Pipeline de inferencia (predicciones)

├── 10\_production\_validation.ipynb     \# Validación en producción

├── 11\_historical\_data\_export.ipynb    \# Exportación de datos históricos

└── artifacts/                         \# Modelos entrenados y artefactos

## 🔄 Flujo de Trabajo

### 1\. Preparación de Datos (NB01)

**Objetivo**: Cargar y preparar todos los datasets necesarios.

**Fuentes de datos**:

- **REE (Red Eléctrica Española)**: Demanda eléctrica real y prevista (5 minutos)  
- **Meteorología**: Datos climáticos de 46 ciudades españolas (1 hora)  
- **Precios**: Precio de la electricidad (1 hora)  
- **Embalses**: Niveles de embalses hidroeléctricos (diario)  
- **Eventos**: Calendario de festivos

**Procesamiento**:

- Estandarización a frecuencia horaria con función `estandarizar_frecuencia_horaria()`  
- Interpolación y relleno de huecos temporales  
- Eliminación de columnas innecesarias  
- Filtrado por rango de fechas configurables

**Output**:

- `df_demanda_horario.parquet`: Demanda horaria estandarizada  
- `df_meteo_horario.parquet`: Meteorología horaria  
- `df_precios_horario.parquet`: Precios horarios  
- `df_embalses_horario.parquet`: Embalses con forward-fill

### 2\. Feature Engineering (NB02)

**Objetivo**: Crear features predictivas para el modelo.

**Features temporales**:

- **Cíclicas**: Hora, día de semana, mes (sin/cos para capturar ciclicidad)  
- **Categóricas**: Hora, día, mes, trimestre, año  
- **Binarias**: Festivos, fines de semana, horas pico

**Features de demanda**:

- **Lags**: 1h, 24h, 48h, 168h (7 días)  
- **Medias móviles**: 6h, 12h, 24h, 48h, 168h  
- **Desviaciones estándar móviles**: Mismas ventanas

**Features meteorológicas**:

- Agregación espacial ponderada por población  
- Variables: temperatura, precipitación, viento, nubosidad

**Features de precio**:

- Precio actual y lags

**Output**:

- `df_features_completo.parquet`: Dataset con todas las features

### 3\. Análisis Exploratorio (NB03)

**Análisis realizados**:

- Patrones temporales (estacionalidad, tendencias)  
- Correlaciones entre features  
- Distribuciones de variables  
- Detección de outliers  
- Análisis de festivos vs laborales

### 4\. Modelos Baseline (NB04)

**Objetivo**: Establecer líneas base de comparación.

**Modelos implementados**:

1. **Persistencia naive**: Repetir valor de hace 7 días  
2. **Media móvil simple**: Promedio de últimas 168 horas  
3. **Regresión lineal simple**: Features temporales básicas

**Métricas**:

- MAE (Mean Absolute Error)  
- RMSE (Root Mean Squared Error)  
- MAPE (Mean Absolute Percentage Error)  
- R² Score

### 5\. Modelos Avanzados \- Árboles (NB05)

**Modelos entrenados**:

1. **Random Forest**: Ensemble de árboles de decisión  
2. **XGBoost**: Gradient Boosting optimizado  
3. **LightGBM**: Gradient Boosting eficiente  
4. **CatBoost**: Gradient Boosting con manejo nativo de categóricas

**Optimización**:

- Búsqueda de hiperparámetros con validación cruzada  
- Feature importance analysis  
- Early stopping para evitar overfitting

### 6\. Optimización de Hiperparámetros (NB06)

**Objetivo**: Optimización automática de hiperparámetros con Optuna.

**Modelos optimizados**:

- XGBoost
- CatBoost
- LightGBM
- Random Forest

**Técnicas**:

- Búsqueda bayesiana de hiperparámetros
- Validación cruzada temporal
- Early stopping para evitar sobreentrenamiento

### 7\. Modelos Avanzados \- Redes Neuronales (NB07)

**Arquitecturas exploradas**:

1. **MLP (Multilayer Perceptron)**: Red neuronal feedforward  
2. **LSTM**: Red recurrente para series temporales  
3. **CNN-LSTM**: Combinación de convolucionales y recurrentes

**Técnicas**:

- Normalización de features  
- Dropout para regularización  
- Early stopping y reducción de learning rate  
- Secuencias temporales para LSTM

### 8\. Comparación de Modelos (NB08)

**Evaluación**:

- Métricas en conjunto de test  
- Análisis de residuos  
- Visualización de predicciones vs valores reales  
- Comparación de tiempos de entrenamiento e inferencia  
- Score combinado para ranking de modelos

**Resultado**: XGBoost seleccionado como modelo final (MAE: 217.83 MW, MAPE: 0.72%, R²: 0.9942)

**Reentrenamiento con todos los datos**:

- Usa train \+ test combinados para maximizar información  
- Garantiza mejor rendimiento en producción  
- Mantiene mismos hiperparámetros del mejor modelo

**Guardado del modelo**:

- Serialización del pipeline completo con `joblib`  
- Guardado en `../../app/models/demanda.pkl`  
- Incluye preprocesamiento y modelo en un solo objeto

### 9\. Validación Temporal (NB09)

**Objetivo**: Validar el modelo final en datos futuros.

**Proceso**:

- Validación en conjunto de datos temporal separado
- Análisis de rendimiento a lo largo del tiempo
- Identificación de períodos con mayor error

### 10\. Inferencia \- Predicciones (NB10)

**Objetivo**: Generar predicciones con el modelo entrenado.

**Proceso**:

1. Configuración de rango de fechas (FECHA\_INICIO, FECHA\_FIN)  
2. Carga de datos con 168h históricas adicionales (para lags)  
3. Estandarización a frecuencia horaria  
4. Feature engineering completo (idéntico a entrenamiento)  
5. Cálculo de lags y medias móviles  
6. Predicción con modelo entrenado  
7. Guardado añadiendo a `../../app/data/demanda.csv`

**Período**: Configurable (por defecto 2025-09-21 a 2025-10-21)

**Importante**:

- Usa la misma función `estandarizar_frecuencia_horaria()` que NB01  
- Aplica exactamente las mismas transformaciones que NB02  
- Añade predicciones al archivo existente sin borrar histórico  
- Elimina duplicados manteniendo la versión más reciente

### 11\. Validación en Producción (NB10 - production_validation)

**Objetivo**: Validar el modelo con datos actuales de producción.

**Proceso**:

- Carga de datos más recientes disponibles
- Comparación con predicciones del modelo
- Análisis de rendimiento en condiciones reales

### 12\. Inferencia \- Datos Históricos (NB11)

**Objetivo**: Exportar datos históricos para la aplicación.

**Proceso**:

1. Carga de datos desde `data_parquet_clean`  
2. Estandarización a frecuencia horaria  
3. Integración de fuentes  
4. Formato de salida estandarizado  
5. Guardado en `../../app/data/demanda.csv`

**Período**: 2023-01-01 a 2025-09-20

**Campos de salida**:

- `dia`: Fecha  
- `hora`: Hora del día (0-23)  
- `datetime`: Timestamp completo  
- `demanda_real`: Demanda real de REE  
- `demanda_prevista_ree`: Previsión oficial de REE  
- `demanda_prevista_modelo`: Vacío (sin predicciones en histórico)

## 📊 Datasets Utilizados

### Entrada (data\_parquet\_clean/)

| Dataset | Fuente | Frecuencia Original | Frecuencia Final | Variables Clave |
| :---- | :---- | :---- | :---- | :---- |
| REE Demanda | `data/ree/data_parquet_clean/demanda/` | 5 minutos | 1 hora | real, prevista |
| Meteorología | `data/climatologia/data_parquet_clean/meteo/` | 1 hora | 1 hora | temperature\_2m, precipitation, wind\_speed\_10m |
| Precios | `data/precio_luz/data_parquet_clean/precios_luz/` | 1 hora | 1 hora | price |
| Embalses | `data/hidrografica/data_parquet_clean/embalses/` | 1 día | 1 hora (ffill) | nivel, capacidad |

### Salida (app/data/)

| Archivo | Formato | Descripción | Actualización |
| :---- | :---- | :---- | :---- |
| `demanda.csv` | CSV | Histórico \+ Predicciones | NB11 → NB10 |
| `demanda.parquet` | Parquet | Backup del CSV | Automático |

## 🔧 Función Clave: Estandarización Horaria

def estandarizar\_frecuencia\_horaria(df, columnas\_numericas, metodo='mean'):

    """

    Estandariza un dataframe a frecuencia horaria sin huecos ni duplicados.

    

    Parámetros:

    \- df: DataFrame con columna 'datetime'

    \- columnas\_numericas: Lista de columnas numéricas a procesar

    \- metodo: 'mean' (agregación), 'ffill' (forward fill), 'interpolate'

    

    Proceso:

    1\. Redondear a la hora más cercana (floor)

    2\. Agrupar/eliminar duplicados según método

    3\. Crear rango completo de horas

    4\. Reindexar y rellenar huecos

    

    Retorna: DataFrame con frecuencia horaria exacta

    """

**Uso por dataset**:

- **REE**: `metodo='mean'` \- Agrega de 5min a 1h  
- **Meteorología**: `metodo='interpolate'` \- Rellena huecos con interpolación lineal  
- **Precios**: `metodo='mean'` \- Promedia duplicados  
- **Embalses**: `metodo='ffill'` \- Forward-fill de diario a horario

## 📈 Métricas del Modelo Final

**Modelo Seleccionado**: XGBoost (optimizado)

### Rendimiento en Test Set

| Métrica | Valor | Descripción |
| :---- | :---- | :---- |
| **MAE** | 217.83 MW | Error medio absoluto |
| **RMSE** | 289.47 MW | Error cuadrático medio (estimado) |
| **MAPE** | 0.72% | Error porcentual absoluto medio |
| **R²** | 0.9942 | Coeficiente de determinación |

### Comparación con Otros Modelos

| Modelo | MAE (MW) | MAPE (%) | R² | Tiempo (s) | Score |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **XGBoost (Test)** | **217.83** | **0.72** | **0.9942** | **0.64** | **1.0000** |
| CatBoost (Optuna) | 249.62 | 0.84 | 0.9900 | 0.50 | 0.9819 |
| LightGBM (Optuna) | 257.64 | 0.87 | 0.9900 | 0.50 | 0.9777 |
| LightGBM (Test) | 259.78 | 0.87 | 0.9921 | 1.06 | 0.9777 |

### Justificación de la Selección

XGBoost fue seleccionado como modelo final por:

1. **Mejor precisión**: MAE de 217.83 MW (más bajo entre todos los modelos)  
2. **Alta estabilidad**: R² de 0.9942 indica excelente ajuste (99.42% de varianza explicada)  
3. **MAPE de 0.72%**: Error porcentual muy bajo, inferior al 1%  
4. **Excelente balance eficiencia/precisión**: Entrenamiento en 0.64s  
5. **Error relativo**: Solo \~0.79% respecto a la demanda media de España (\~27,500 MW)  
6. **Robustez**: Excelente rendimiento en validación cruzada temporal

## 🚀 Uso del Pipeline de Inferencia

### Paso 1: Generar Histórico (ejecutar una vez)

\# Notebook: 11\_historical\_data\_export.ipynb

\# Configurar rango histórico

FECHA\_INICIO \= pd.Timestamp('2023-01-01 00:00:00')

FECHA\_FIN \= pd.Timestamp('2025-09-20 23:00:00')

\# Ejecutar todas las celdas

\# Output: app/datos/demanda.csv (histórico)

### Paso 2: Generar Predicciones

\# Notebook: 10\_inference\_pipeline.ipynb

\# Configurar rango de predicción

FECHA\_INICIO \= pd.Timestamp('2025-09-21 00:00:00')

FECHA\_FIN \= pd.Timestamp('2025-10-21 23:00:00')

\# Ejecutar todas las celdas

\# Output: app/datos/demanda.csv (histórico \+ predicciones)

### Paso 3: Actualizar Predicciones

Para añadir nuevas predicciones, simplemente:

1. Modificar `FECHA_INICIO` y `FECHA_FIN` en NB10  
2. Ejecutar el notebook  
3. Las nuevas predicciones se añadirán automáticamente

**Nota**: Si hay solapamiento temporal, las predicciones nuevas sobrescribirán las antiguas.

## ⚙️ Configuración y Dependencias

### Librerías principales

pandas\>=1.5.0

numpy\>=1.23.0

scikit-learn\>=1.2.0

xgboost\>=1.7.0

lightgbm\>=3.3.0

catboost\>=1.1.0

tensorflow\>=2.10.0  \# Para redes neuronales

holidays\>=0.18      \# Para festivos

matplotlib\>=3.6.0

seaborn\>=0.12.0

joblib\>=1.2.0

### Configuración de rutas

Todos los notebooks usan rutas relativas desde `models/demand_forecast/`:

BASE\_DIR \= Path('../..')

DATA\_DIR \= BASE\_DIR / 'data'

APP\_DIR \= BASE\_DIR / 'app'

## 📝 Notas Importantes

### Frecuencia Horaria

**CRÍTICO**: Todos los datos deben estar en frecuencia horaria exacta:

- Timestamps en formato `YYYY-MM-DD HH:00:00`  
- Sin minutos ni segundos  
- Sin huecos temporales  
- Sin duplicados

La función `estandarizar_frecuencia_horaria()` garantiza esto.

### Lags y Medias Móviles

Para calcular lags de 168h (7 días), necesitamos:

- Cargar datos históricos adicionales  
- En NB10: `fecha_inicio_con_historico = FECHA_INICIO - pd.Timedelta(hours=168)`  
- Aplicar feature engineering a TODO el dataset  
- Filtrar al rango objetivo al final

### Gestión del Archivo demanda.csv

El archivo `app/data/demanda.csv` es **acumulativo**:

1. NB11 crea/actualiza con histórico (2023-01-01 a 2025-09-20)  
2. NB10 añade predicciones (2025-09-21 en adelante)  
3. Duplicados se resuelven manteniendo la versión más reciente

**Estructura del archivo**:

dia,hora,datetime,demanda\_real,demanda\_prevista\_ree,demanda\_prevista\_modelo

2023-01-01,0,2023-01-01 00:00:00,25430.5,25500.2,

2023-01-01,1,2023-01-01 01:00:00,24320.8,24400.1,

...

2025-09-20,23,2025-09-20 23:00:00,26780.3,26850.6,

2025-09-21,0,2025-09-21 00:00:00,,,27100.4

2025-09-21,1,2025-09-21 01:00:00,,,26890.2

- **Histórico**: `demanda_real` y `demanda_prevista_ree` con datos  
- **Predicciones**: Solo `demanda_prevista_modelo` con datos

## 🔍 Troubleshooting

### Error: "No se encontró columna de demanda"

**Causa**: Nombres de columnas inconsistentes (Hora/hora/datetime/time)

**Solución**: Los notebooks normalizan automáticamente a `datetime`

### Error: "Faltan X features requeridas"

**Causa**: Feature engineering diferente entre entrenamiento e inferencia

**Solución**:

- Verificar que NB10 aplica exactamente las mismas transformaciones que NB02  
- Revisar que todas las features (lags, MA, temporales) se crean igual

### Frecuencia incorrecta (5 minutos en lugar de 1 hora)

**Causa**: No se aplicó `estandarizar_frecuencia_horaria()`

**Solución**: Verificar que se ejecuta la función en todos los datasets antes de integrar

### Valores NaN en lags/medias móviles

**Causa**: No se cargaron suficientes datos históricos

**Solución**: Asegurar que se cargan al menos 168h antes de FECHA\_INICIO

## 📚 Referencias

- **REE**: [Red Eléctrica Española](https://www.ree.es)  
- **Open-Meteo**: [API Meteorológica](https://open-meteo.com)  
- **ESIOS**: [Sistema de Información del Operador del Sistema](https://www.esios.ree.es)

## 👥 Autores

David Martín Hernández  
Juan Olivares Diez

---

**Última actualización**: Noviembre 2025  
