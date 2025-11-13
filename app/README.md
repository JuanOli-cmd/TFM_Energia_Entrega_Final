# ⚡ Panel Energético España

Aplicación web interactiva desarrollada con Streamlit para visualizar y analizar la demanda eléctrica y los precios de la luz para hogares en España.

## 🎯 Características

### ⚡ Demanda Eléctrica

#### 📊 Demanda Eléctrica
- Visualización de demanda real, previsión de REE y previsión de nuestro modelo
- Selector: un día específico o período personalizable
- Métricas clave: demanda promedio, máxima, mínima, MAE del modelo
- Distribución horaria de la demanda
- Gráficos interactivos con Plotly

#### 🔮 Comparación de Modelos
- Comparación entre el modelo REE y nuestro modelo predictivo de demanda
- Métricas de error: MAE, RMSE, MAPE
- Visualización de la evolución de errores
- Distribución estadística de errores
- Box plots y histogramas comparativos
- Análisis de mejora porcentual

#### 📈 Análisis Temporal
- Análisis de demanda por día de la semana
- Mapa de calor: patrones de demanda por día y hora
- Identificación de patrones semanales y horarios
- Estadísticas con desviación estándar

### 💰 Precio de la Luz

#### 💰 Precio de la Luz
- Visualización de precios históricos para hogares (€/kWh)
- Selector: un día específico o período personalizable
- **Para un día**: Gráfico de barras con escala de colores (verde=bajo, rojo=alto)
- **Para período**: Gráfico de líneas temporal
- Métricas: precio promedio, máximo, mínimo, volatilidad
- Distribución horaria del precio con rangos min-max
- Precios en rango realista: 0.08 - 0.40 €/kWh

#### 💡 Predicción Precio Luz
- Comparación precio real vs predicho (predicciones desde 2025-09-21)
- Métricas de precisión: MAE, RMSE, MAPE, R²
- Gráfico comparativo de series temporales
- Evolución del error de predicción
- Distribución de errores (histograma y boxplot)
- Scatter plot: Real vs Predicho con línea de predicción perfecta
- Análisis de calidad del modelo predictivo

## 🚀 Instalación

### Requisitos previos
- Python 3.9 o superior
- pip

### Pasos de instalación

1. Instalar dependencias:
```bash
pip install -r ../requirements.txt
```

O instalar solo las dependencias de la app:
```bash
pip install streamlit plotly pandas numpy
```

## 📊 Datos

Los datos se encuentran en el directorio `app/data/`:

### Demanda Eléctrica (`demanda.csv`)
- **Campos**:
  - `dia`: Fecha
  - `hora`: Hora del día (0-23)
  - `datetime`: Timestamp completo
  - `demanda_real`: Demanda real (MW)
  - `demanda_prevista_ree`: Previsión de REE (MW)
  - `demanda_prevista_modelo`: Previsión de nuestro modelo (MW)
- **Período histórico**: 2023-01-01 a 2025-09-20
- **Predicciones desde**: 2025-09-21 en adelante
- **Frecuencia**: Horaria
- **Geografía**: España - Península

### Precio de la Luz (`precio_luz.csv`)
- **Campos**:
  - `dia`: Fecha
  - `hora`: Hora del día (0-23)
  - `precio_real`: Precio real para hogares (€/kWh)
  - `precio_predicho`: Precio predicho por nuestro modelo (€/kWh)
- **Período completo**: 2023-01-01 a 2025-10-21
- **Predicciones desde**: 2025-09-21 (744 registros con predicción)
- **Registros totales**: 24,600
- **Frecuencia**: Horaria
- **Rango de precios**: 0.08 - 0.40 €/kWh (realista para hogares españoles)
- **Geografía**: España - Tarifa para hogares

## 🎮 Uso

Para ejecutar la aplicación:

```bash
cd app
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 🖼️ Funcionalidades por sección

### ⚡ Demanda Eléctrica

#### 📊 Demanda Eléctrica
- Selecciona un día específico o un rango de fechas
- Visualiza tres series temporales simultáneamente (Real, REE, Modelo)
- Analiza patrones horarios promedio con rangos min-max
- Identifica picos de demanda con timestamp exacto

#### 🔮 Comparación de Modelos
- Selecciona el período de análisis (últimos 7 días, mes, 3 meses, todo)
- Compara métricas de precisión entre REE y nuestro modelo
- Visualiza mejora porcentual del modelo
- Analiza la distribución de errores con histogramas
- Identifica en qué condiciones cada modelo funciona mejor

#### 📈 Análisis Temporal
- Descubre patrones semanales (lunes a domingo)
- Identifica horas de mayor y menor demanda
- Utiliza el mapa de calor para visualizar patrones día-hora
- Analiza comportamiento por día de la semana

### 💰 Precio de la Luz

#### 💰 Precio de la Luz
- Selecciona un día específico para ver precios por hora (gráfico de barras)
- O selecciona un período para análisis temporal (gráfico de líneas)
- Identifica las horas más baratas y más caras
- Visualiza el precio medio del período
- Analiza la volatilidad de precios
- Optimiza tu consumo eléctrico según tarifas horarias

#### 💡 Predicción Precio Luz
- Evalúa la precisión del modelo predictivo
- Compara precios reales vs predichos visualmente
- Analiza el error de predicción a lo largo del tiempo
- Identifica sesgos en las predicciones
- Utiliza el scatter plot para evaluar correlación
- Métricas estadísticas completas (MAE, RMSE, MAPE, R²)

## 🛠️ Tecnologías

- **Streamlit**: Framework para aplicaciones web
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Manipulación de datos
- **NumPy**: Cálculos numéricos

## 📝 Notas

- Los gráficos son completamente interactivos (zoom, pan, hover)
- Los datos se cargan en caché para mejorar el rendimiento
- La aplicación es responsive y se adapta a diferentes tamaños de pantalla
- Los precios están en €/kWh (formato para hogares), no en €/MWh
- El menú lateral está organizado por secciones: Demanda y Precios

## 💡 Casos de Uso

### Para análisis de demanda:
- Identificar patrones de consumo eléctrico nacional
- Evaluar la precisión de modelos predictivos vs REE
- Planificar generación eléctrica basada en patrones históricos
- Analizar picos de demanda para gestión de red

### Para análisis de precios:
- Planificar consumo eléctrico en hogares según tarifas
- Identificar las mejores horas para consumir electricidad
- Evaluar ahorro potencial con discriminación horaria
- Analizar volatilidad y tendencias de precios
- Validar modelos de predicción de precios

## 🐛 Solución de problemas

### Error al cargar datos
Asegúrate de que los archivos existen:
- `data/demanda.csv`
- `data/precio_luz.csv`

Y tienen el formato correcto con las columnas especificadas.

### Problemas de rendimiento
Si la aplicación es lenta con grandes períodos de tiempo, intenta seleccionar rangos más pequeños.

### Datos no se actualizan
Limpia la caché de Streamlit: presiona 'C' en la aplicación o reinicia el servidor.

## 📧 Soporte

Para reportar problemas o sugerencias, por favor crea un issue en el repositorio.
