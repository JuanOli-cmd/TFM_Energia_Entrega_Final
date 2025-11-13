# ⚙️ Predicción del Precio de la Electricidad — Proyecto TFM

Este documento agrupa los tres notebooks principales del proyecto orientado a la **predicción, inferencia y validación del precio horario de la electricidad** en el mercado ibérico.

---

## 📘 1. Predicción — `Prediccion_precio_luz.ipynb`

Este notebook constituye el **núcleo de modelado** del sistema predictivo. Implementa todo el flujo de análisis, entrenamiento y evaluación de modelos para estimar el precio horario de la electricidad.

### 🧩 Estructura del notebook
1. **Carga y preparación de datos**
   - Lectura de datasets históricos 2024‑2025 en formato `.parquet` desde `data/precio_luz (1)/data_parquet_clean/precios_luz/` y datos REE.
   - Estandarización de nombres de columnas (`Día`, `Hora`, `Precio`, `Demanda`, etc.).
   - Conversión de tipos (`string` → `timestamp`) y creación de índices temporales.
   - Alineación temporal con `merge_asof` para unir señales a distintas frecuencias.

2. **Análisis exploratorio (EDA)**
   - Estadísticas descriptivas, correlaciones y patrones estacionales.
   - Análisis de demanda, producción renovable y precios marginales.
   - Visualización de tendencias y autocorrelaciones.

3. **Preprocesamiento**
   - Limpieza de valores nulos y outliers.
   - Generación de *features* derivadas (lags, medias móviles, variables de calendario).
   - División en *train/validation/test*.

4. **Modelado**
   - Entrenamiento y comparación de múltiples modelos:
     - **Baselines**: Naive, Seasonal Naive, Media Móvil
     - **SARIMAX** — para captura de estacionalidad
     - **XGBoost** — para relaciones no lineales (modelo final seleccionado)
     - **LightGBM** — alternativa de gradient boosting
     - **LSTM / GRU** — para dependencias secuenciales
   - Evaluación mediante MAE, RMSE, MAPE y R²
   - **Modelo final**: XGBoost (guardado como `precio_luz_xgb.pkl`)

5. **Validación y visualización**
   - Comparación entre precios reales y predichos.
   - Gráficos de error, dispersión y desempeño temporal.
   - Exportación de métricas y modelos finales (`.pkl`, `.h5`).

6. **Exportación**
   - Guardado de modelos, escaladores y transformadores para la fase de inferencia.

---

## 🧠 2. Inferencia — `Inferencia_precio_luz.ipynb`

Este cuaderno representa la **fase operativa** del sistema: utiliza los modelos entrenados para generar predicciones sobre nuevos datos horarios o diarios.

### 🔧 Estructura del notebook
1. **Carga del modelo entrenado**
   - Importa los modelos y escaladores generados en la fase anterior.
   - Verificación de versiones y consistencia de features.

2. **Carga de datos recientes**
   - Ingesta de datos de entrada actualizados (REE, OMIE, AEMET, etc.).
   - Limpieza y preparación automática según el mismo pipeline de preprocesado.

3. **Generación de predicciones**
   - Aplicación del modelo óptimo seleccionado.
   - Obtención de precios previstos por hora o por día.
   - Posibilidad de predicción multihoraria o rolling window.

4. **Visualización y exportación**
   - Representación gráfica de resultados (curvas reales vs. predichas).
   - Exportación de resultados a `.csv` o `.json` para su análisis posterior.

5. **Integración**
   - Preparación para conexión con APIs o dashboards externos.
   - Base para la automatización de inferencias diarias o en tiempo real.

---

## 🔍 3. Validación — `Precio_luz_validacion.ipynb`

Este notebook cierra el ciclo del proyecto y se centra en la **validación integral del modelo** a partir de las predicciones generadas.

### 📊 Contenidos principales
1. **Evaluación comparativa**
   - Revisión de métricas globales (MAE, RMSE, MAPE, R²).
   - Comparación entre modelos entrenados (SARIMAX, XGBoost, LightGBM, LSTM, GRU).
   - Validación del modelo final seleccionado (XGBoost) en período de control (15-21 septiembre 2025).

2. **Análisis de errores**
   - Identificación de patrones de desviación.
   - Estudio de periodos con alta volatilidad o anomalías.

3. **Visualización de desempeño**
   - Curvas de predicción vs. valores reales.
   - Mapas de calor horarios y gráficos de dispersión.

4. **Conclusiones**
   - Resumen del comportamiento del sistema.
   - Discusión de fortalezas, limitaciones y posibles mejoras.

5. **Exportación de resultados**
   - Generación de informes gráficos y tablas de métricas finales.

---

## 📚 Créditos

- **Autor:** Jorge Rodríguez  
- **Máster:** Inteligencia Artificial Generativa (MBIT School)  
- **Proyecto:** Predicción del Precio de la Luz — Iberian Market  
- **Lenguaje:** Python 3.x  
- **Formato:** Jupyter Notebook (`.ipynb`)  
- **Año:** 2025  

---

## 💡 Próximos pasos

- Implementar *ensembles* híbridos combinando modelos estadísticos y neuronales.  
- Ajuste fino de hiperparámetros con optimización bayesiana.  
- Despliegue de inferencia diaria automatizada con alertas de precios.  
- Generación de un dashboard de visualización interactiva.

---

> Este documento consolida los tres cuadernos fundamentales del proyecto, representando el flujo completo: **Predicción → Inferencia → Validación** del precio eléctrico en el mercado ibérico.
