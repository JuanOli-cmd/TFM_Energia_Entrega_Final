# Modelo de Predicción de Precios de la Luz

Este directorio contiene el desarrollo completo de un modelo de Machine Learning y Deep Learning para predecir el precio horario de la electricidad en España.

## 📁 Estructura del Proyecto

```
Precio de la luz/
├── Prediccion_precio_luz.ipynb    # Entrenamiento y optimización de modelos
├── Precio_luz_validacion.ipynb    # Validación del modelo final
├── Inferencia_precio_luz.ipynb    # Pipeline de inferencia para producción
└── README.md                       # Este archivo
```

## 🔄 Flujo de Trabajo

### 1. Predicción (Entrenamiento) - `Prediccion_precio_luz.ipynb`

**Objetivo**: Entrenar y optimizar múltiples modelos predictivos de precios horarios.

**Proceso**:

1. **Carga de datos**:
   - Precios: `datasets/precios_luz_2024.parquet`, `datasets/precios_luz_2025.parquet`
   - REE: `datasets/df_ree.parquet` (demanda, generación, emisiones, almacenamiento)

2. **Preprocesamiento**:
   - Limpieza y normalización de timestamps
   - Eliminación de duplicados
   - Interpolación de faltantes
   - Alineación temporal con `merge_asof` (tolerancia ±1h)

3. **Feature Engineering**:
   - **Lags y Rolling Features**: `price_lag[1,2,3,24,48,168]`, medias y desviaciones móviles (ventanas 3h, 6h, 24h)
   - **Variables del sistema eléctrico**: `dem_real`, `gen_ciclo_combinado`, `emis_ciclo_combinado`, `gen_solar_fotovoltaica`, `alm_entrega_de_baterias`, etc.
   - **Calendario y estacionalidad**: `hour`, `dow`, `is_weekend`, codificación trigonométrica (`hour_sin/cos`, `dow_sin/cos`)
   - **Series de Fourier**: `fourier_w_sin[k]`, `fourier_w_cos[k]` para estacionalidad anual/semanal
   - **Indicadores de missing**: sufijo `_isna` en columnas lag/rolling

4. **Partición temporal**:
   - Train: hasta fecha configurable
   - Valid: período intermedio
   - Test: período final

5. **Modelos entrenados**:
   - **Baselines**: Naive, Seasonal Naive, Media móvil
   - **SARIMAX**: Modelo estacional con exógenas
   - **XGBoost**: Gradient Boosting optimizado
   - **LSTM**: Red neuronal recurrente
   - **GRU**: Red neuronal recurrente

6. **Selección del mejor modelo**:
   - Comparación basada en MAE en conjunto TEST
   - Modelo seleccionado: **XGBoost**

**Salidas**:
- `precio_luz_xgb.pkl`: Modelo final guardado como bundle robusto
- `optimization_results.csv`: Resultados de optimización
- `baselines_metrics.csv`: Métricas de todos los modelos
- `model_ranking_TEST.csv`: Ranking de modelos según métricas

### 2. Validación - `Precio_luz_validacion.ipynb`

**Objetivo**: Validar el modelo final seleccionado (XGBoost) en período de control.

**Proceso**:

1. Carga del modelo (`precio_luz_xgb.pkl`) y datos parquet
2. Limpieza, ordenamiento temporal y fusión tolerante con `merge_asof`
3. Regeneración automática de features esperadas
4. Reconstrucción del booster desde `booster_json`
5. Creación de `df_valid` filtrado por rango de validación (15-21 septiembre 2025)
6. Generación de predicciones (`predicted_price`) y trazado comparativo

**Salidas**:
- Figura: precios reales vs predichos
- `validation_predictions.csv`: Predicciones horarias
- `validation_daily_summary.csv`: Errores medios diarios

### 3. Inferencia - `Inferencia_precio_luz.ipynb`

**Objetivo**: Pipeline de inferencia para producción (predicción diaria).

**Proceso**:

1. Carga automática del modelo (`precio_luz_xgb.pkl`)
2. Lectura y preprocesado de datos actuales (últimas 24-48h)
3. Generación de features compatibles y predicción inmediata
4. Exportación de resultados a `precio_luz.csv`

**Formato de salida** (`precio_luz.csv`):
```
dia,hora,precio_real,precio_predicho
2025-09-22,00,0.10,0.09
2025-09-22,01,0.10,0.09
...
```

Diseñado para integrarse en dashboard local o API FastAPI/Streamlit.

## 📊 Datasets Utilizados

### Entrada

| Dataset | Fuente | Frecuencia | Variables Clave |
| :---- | :---- | :---- | :---- |
| Precios | `datasets/precios_luz_2024.parquet`, `datasets/precios_luz_2025.parquet` | Horaria | `price` |
| REE Demanda | `datasets/df_ree.parquet` | Horaria | `dem_real`, `dem_prevista` |
| REE Generación | `datasets/df_ree.parquet` | Horaria | `gen_ciclo_combinado`, `gen_solar_fotovoltaica`, etc. |
| REE Emisiones | `datasets/df_ree.parquet` | Horaria | `emis_ciclo_combinado`, etc. |
| REE Almacenamiento | `datasets/df_ree.parquet` | Horaria | `alm_entrega_de_baterias`, etc. |

### Salida

| Archivo | Formato | Descripción | Actualización |
| :---- | :---- | :---- | :---- |
| `precio_luz_xgb.pkl` | PKL (Joblib) | Modelo final XGBoost | Prediccion_precio_luz.ipynb |
| `precio_luz.csv` | CSV | Predicciones para app | Inferencia_precio_luz.ipynb |

## 📈 Métricas del Modelo Final

**Modelo Seleccionado**: XGBoost

### Rendimiento en Test Set

| Métrica | Valor | Descripción |
| :---- | :---- | :---- |
| **MAE** | 7.377 €/MWh | Error medio absoluto |
| **RMSE** | 11.844 €/MWh | Error cuadrático medio |
| **MAPE** | 5.59% | Error porcentual absoluto medio |

### Comparación con Otros Modelos

| Modelo | MAE (€/MWh) | RMSE (€/MWh) | MAPE (%) | Observaciones |
| :---- | :---- | :---- | :---- | :---- |
| **XGBoost** 🏆 | **7.377** | **11.844** | **5.59** | Modelo final seleccionado |
| SARIMAX-lite | 41.355 | 47.066 | 32.63 | Rendimiento débil |
| LSTM | Variable | Variable | Variable | Requiere GPU |
| GRU | Variable | Variable | Variable | Requiere GPU |

### Justificación de la Selección

XGBoost fue seleccionado como modelo final por:

1. **Mejor precisión**: MAE de 7.377 €/MWh (más bajo entre todos los modelos)
2. **Alta estabilidad**: MAPE de 5.59% indica excelente ajuste
3. **Excelente balance eficiencia/precisión**: Entrenamiento rápido
4. **Robustez**: Excelente rendimiento en validación cruzada temporal
5. **Facilidad de despliegue**: Sin dependencias pesadas (TensorFlow, PyTorch)

## 🚀 Uso del Pipeline

### Paso 1: Entrenar Modelos

```bash
cd "models/Precio de la luz"
jupyter notebook Prediccion_precio_luz.ipynb
```

Ejecutar todas las celdas. Esto generará:
- `precio_luz_xgb.pkl`: Modelo final
- `baselines_metrics.csv`: Métricas de todos los modelos
- `model_ranking_TEST.csv`: Ranking de modelos

### Paso 2: Validar Modelo Final

```bash
jupyter notebook Precio_luz_validacion.ipynb
```

Ejecutar todas las celdas. Esto generará:
- `validation_predictions.csv`: Predicciones horarias
- `validation_daily_summary.csv`: Resumen diario de errores

### Paso 3: Generar Predicciones (Inferencia)

```bash
jupyter notebook Inferencia_precio_luz.ipynb
```

Ejecutar todas las celdas. Esto generará:
- `precio_luz.csv`: Predicciones para la aplicación

## ⚙️ Configuración y Dependencias

### Librerías principales

```
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
xgboost>=1.7.0
statsmodels>=0.13.0  # Para SARIMAX
torch>=1.12.0         # Para LSTM/GRU (opcional)
joblib>=1.2.0
pyarrow>=10.0.0
matplotlib>=3.6.0
```

### Configuración de rutas

Todos los notebooks usan rutas relativas desde `models/Precio de la luz/`:

```python
DATA_DIR = "datasets"  # Ajustar según estructura del proyecto
```

**Nota**: Las rutas pueden necesitar ajuste según la estructura real del proyecto. Los notebooks esperan encontrar los datos en `datasets/` relativo a su ubicación.

## 📝 Notas Importantes

### Alineación Temporal

**CRÍTICO**: Los datos de diferentes fuentes (precios, REE) pueden tener diferentes frecuencias o timestamps ligeramente desalineados. El pipeline usa `merge_asof` con tolerancia de ±1h para alinear correctamente las señales.

### Features y Missing Values

El modelo XGBoost puede manejar valores faltantes nativamente, pero se añaden indicadores `_isna` para mejorar la robustez. Si faltan features en inferencia, el script las crea automáticamente con valor 0.

### Unidades

- **Entrenamiento/Validación**: Los precios están en €/MWh
- **Aplicación**: Los precios se convierten a €/kWh para visualización (dividir por 1000)

## 🔍 Troubleshooting

### Error: "No se encontró el archivo: datasets/..."

**Causa**: Rutas incorrectas o estructura de carpetas diferente

**Solución**: Ajustar `DATA_DIR` o `RAW_DIR` en los notebooks según la estructura real del proyecto.

### Error: "Faltan X columnas que el modelo espera"

**Causa**: Feature engineering diferente entre entrenamiento e inferencia

**Solución**: 
- Verificar que se aplican exactamente las mismas transformaciones
- El script de validación crea automáticamente columnas faltantes con valor 0

### Error al cargar modelo: "booster_json not found"

**Causa**: El archivo `precio_luz_xgb.pkl` está corrupto o incompleto

**Solución**: Reentrenar el modelo ejecutando `Prediccion_precio_luz.ipynb` completo.

## 📚 Referencias

- **OMIE**: [Operador del Mercado Ibérico de Energía](https://www.omie.es/)
- **ESIOS**: [Sistema de Información del Operador del Sistema](https://www.esios.ree.es/)
- **REE**: [Red Eléctrica Española](https://www.ree.es)

## 👥 Autores

David Martín Hernández  
Juan Olivares Diez

---

**Última actualización**: Noviembre 2025

