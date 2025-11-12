import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Panel de Demanda Eléctrica España",
    page_icon="⚡",
    layout="wide"
)

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv('data/demanda.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['fecha'] = df['datetime'].dt.date
    return df

@st.cache_data
def cargar_datos_precio():
    df = pd.read_csv('data/precio_luz.csv')
    df['datetime'] = pd.to_datetime(df['dia'].astype(str) + ' ' + df['hora'].astype(str) + ':00:00')
    df['fecha'] = df['datetime'].dt.date
    return df

# Sidebar
st.sidebar.title("⚡ Panel Energético España")
st.sidebar.markdown("---")

# Sección Demanda Eléctrica
st.sidebar.markdown("### ⚡ Demanda Eléctrica")
menu_demanda = ["📊 Demanda Eléctrica", "🔮 Comparación de Modelos", "📈 Análisis Temporal"]

menu_precio = ["💰 Precio de la Luz", "💡 Predicción Precio Luz"]

menu_opciones = menu_demanda + menu_precio

if "boton_seleccionado" not in st.session_state:
    st.session_state.boton_seleccionado = menu_opciones[0]

# Botones de Demanda Eléctrica
for opcion in menu_demanda:
    # Determinar el tipo de botón según si está seleccionado
    tipo_boton = "primary" if st.session_state.boton_seleccionado == opcion else "secondary"
    if st.sidebar.button(
        opcion, 
        use_container_width=True, 
        key=f"btn_{opcion}",
        type=tipo_boton
    ):
        st.session_state.boton_seleccionado = opcion
        st.rerun()

# Separador y Sección Precio de la Luz
st.sidebar.markdown("---")
st.sidebar.markdown("### 💰 Precio de la Luz")

# Botones de Precio de la Luz
for opcion in menu_precio:
    # Determinar el tipo de botón según si está seleccionado
    tipo_boton = "primary" if st.session_state.boton_seleccionado == opcion else "secondary"
    if st.sidebar.button(
        opcion, 
        use_container_width=True, 
        key=f"btn_{opcion}",
        type=tipo_boton
    ):
        st.session_state.boton_seleccionado = opcion
        st.rerun()

boton_seleccionado = st.session_state.boton_seleccionado

# Cargar datos
df = cargar_datos()

# ==================== DEMANDA ELÉCTRICA ====================
if boton_seleccionado == "📊 Demanda Eléctrica":
    st.title("⚡️ Demanda Eléctrica - España Península")
    
    # Selector de tipo de visualización
    col1, col2, col3 = st.columns([2, 2, 4])
    
    with col1:
        tipo_seleccion = st.radio(
            "Tipo de visualización",
            ["Un día", "Período"],
            horizontal=True
        )
    
    # Selector de fechas según el tipo
    fecha_min = df['fecha'].min()
    fecha_max = df['fecha'].max()
    
    if tipo_seleccion == "Un día":
        with col2:
            fecha_seleccionada = st.date_input(
                "Selecciona un día",
                value=fecha_max,
                min_value=fecha_min,
                max_value=fecha_max
            )
        fecha_inicio = fecha_seleccionada
        fecha_fin = fecha_seleccionada
    else:  # Período
        with col2:
            fecha_inicio = st.date_input(
                "Fecha inicio",
                value=fecha_max - timedelta(days=7),
                min_value=fecha_min,
                max_value=fecha_max
            )
        
        with col3:
            fecha_fin = st.date_input(
                "Fecha fin",
                value=fecha_max,
                min_value=fecha_inicio,
                max_value=fecha_max
            )
    
    # Filtrar datos
    df_filtrado = df[(df['fecha'] >= fecha_inicio) & (df['fecha'] <= fecha_fin)].copy()
    
    # Métricas principales
    st.markdown("### 📌 Métricas del Período Seleccionado")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        demanda_promedio = df_filtrado['demanda_real'].mean()
        st.metric("Demanda Promedio", f"{demanda_promedio:,.0f} MW")
    
    with col2:
        demanda_maxima = df_filtrado['demanda_real'].max()
        hora_maxima = df_filtrado[df_filtrado['demanda_real'] == demanda_maxima]['datetime'].iloc[0]
        st.metric("Demanda Máxima", f"{demanda_maxima:,.0f} MW")
        st.caption(f"📅 {hora_maxima.strftime('%d/%m/%Y %H:%M')}")
    
    with col3:
        demanda_minima = df_filtrado['demanda_real'].min()
        hora_minima = df_filtrado[df_filtrado['demanda_real'] == demanda_minima]['datetime'].iloc[0]
        st.metric("Demanda Mínima", f"{demanda_minima:,.0f} MW")
        st.caption(f"📅 {hora_minima.strftime('%d/%m/%Y %H:%M')}")
    
    with col4:
        error_modelo = np.abs(df_filtrado['demanda_real'] - df_filtrado['demanda_prevista_modelo']).mean()
        st.metric("MAE Modelo", f"{error_modelo:,.0f} MW")
    
    st.markdown("---")
    
    # Gráfico principal
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_filtrado['datetime'],
        y=df_filtrado['demanda_real'],
        mode='lines',
        name='Demanda Real',
        line=dict(color='#2E86AB', width=2),
        hovertemplate='<b>Real</b><br>%{x|%d/%m/%Y %H:%M}<br>%{y:,.0f} MW<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_filtrado['datetime'],
        y=df_filtrado['demanda_prevista_ree'],
        mode='lines',
        name='Previsión REE',
        line=dict(color='#F77F00', width=1.5, dash='dash'),
        hovertemplate='<b>REE</b><br>%{x|%d/%m/%Y %H:%M}<br>%{y:,.0f} MW<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_filtrado['datetime'],
        y=df_filtrado['demanda_prevista_modelo'],
        mode='lines',
        name='Previsión Modelo',
        line=dict(color='#06A77D', width=1.5, dash='dot'),
        hovertemplate='<b>Modelo</b><br>%{x|%d/%m/%Y %H:%M}<br>%{y:,.0f} MW<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Demanda Eléctrica: {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}",
        xaxis_title='Fecha y Hora',
        yaxis_title='Demanda (MW)',
        hovermode='x unified',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de distribución horaria
    st.markdown("### 🕙 Distribución Horaria de la Demanda")
    df_filtrado['hora'] = df_filtrado['datetime'].dt.hour
    demanda_horaria = df_filtrado.groupby('hora')['demanda_real'].agg(['mean', 'min', 'max']).reset_index()
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=demanda_horaria['hora'],
        y=demanda_horaria['mean'],
        mode='lines+markers',
        name='Promedio',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=8)
    ))
    
    fig2.add_trace(go.Scatter(
        x=demanda_horaria['hora'],
        y=demanda_horaria['max'],
        mode='lines',
        name='Máximo',
        line=dict(color='#D62828', width=1.5, dash='dash'),
        fill=None
    ))
    
    fig2.add_trace(go.Scatter(
        x=demanda_horaria['hora'],
        y=demanda_horaria['min'],
        mode='lines',
        name='Mínimo',
        line=dict(color='#06A77D', width=1.5, dash='dash'),
        fill='tonexty',
        fillcolor='rgba(46, 134, 171, 0.2)'
    ))
    
    fig2.update_layout(
        title='Patrón de Demanda por Hora del Día',
        xaxis_title='Hora del Día',
        yaxis_title='Demanda (MW)',
        xaxis=dict(tickmode='linear', tick0=0, dtick=2),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# ==================== COMPARACIÓN DE MODELOS ====================
elif boton_seleccionado == "🔮 Comparación de Modelos":
    st.title("🔮 Comparación de Modelos Predictivos")
    
    # Selector de período
    col1, col2 = st.columns([2, 6])
    
    with col1:
        periodo = st.selectbox(
            "Período de análisis",
            ["Últimos 7 días", "Último mes", "Últimos 3 meses", "Todo el período"]
        )
    
    if periodo == "Últimos 7 días":
        dias = 7
    elif periodo == "Último mes":
        dias = 30
    elif periodo == "Últimos 3 meses":
        dias = 90
    else:
        dias = (df['fecha'].max() - df['fecha'].min()).days
    
    fecha_corte = df['fecha'].max() - timedelta(days=dias)
    df_analisis = df[df['fecha'] >= fecha_corte].copy()
    
    # Calcular métricas de error
    df_analisis['error_ree'] = df_analisis['demanda_real'] - df_analisis['demanda_prevista_ree']
    df_analisis['error_modelo'] = df_analisis['demanda_real'] - df_analisis['demanda_prevista_modelo']
    df_analisis['error_abs_ree'] = np.abs(df_analisis['error_ree'])
    df_analisis['error_abs_modelo'] = np.abs(df_analisis['error_modelo'])
    df_analisis['error_pct_ree'] = (df_analisis['error_abs_ree'] / df_analisis['demanda_real']) * 100
    df_analisis['error_pct_modelo'] = (df_analisis['error_abs_modelo'] / df_analisis['demanda_real']) * 100
    
    # Métricas comparativas
    st.markdown("### 📊 Métricas de Precisión")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### REE")
        mae_ree = df_analisis['error_abs_ree'].mean()
        rmse_ree = np.sqrt((df_analisis['error_ree']**2).mean())
        mape_ree = df_analisis['error_pct_ree'].mean()
        
        st.metric("MAE", f"{mae_ree:,.0f} MW")
        st.metric("RMSE", f"{rmse_ree:,.0f} MW")
        st.metric("MAPE", f"{mape_ree:.2f}%")
    
    with col2:
        st.markdown("#### Nuestro Modelo")
        mae_modelo = df_analisis['error_abs_modelo'].mean()
        rmse_modelo = np.sqrt((df_analisis['error_modelo']**2).mean())
        mape_modelo = df_analisis['error_pct_modelo'].mean()
        
        st.metric("MAE", f"{mae_modelo:,.0f} MW")
        st.metric("RMSE", f"{rmse_modelo:,.0f} MW")
        st.metric("MAPE", f"{mape_modelo:.2f}%")
    
    with col3:
        st.markdown("#### Mejora")
        mejora_mae = ((mae_ree - mae_modelo) / mae_ree) * 100
        mejora_rmse = ((rmse_ree - rmse_modelo) / rmse_ree) * 100
        mejora_mape = ((mape_ree - mape_modelo) / mape_ree) * 100
        
        st.metric("MAE", f"{mejora_mae:+.1f}%", delta=f"{mejora_mae:.1f}%")
        st.metric("RMSE", f"{mejora_rmse:+.1f}%", delta=f"{mejora_rmse:.1f}%")
        st.metric("MAPE", f"{mejora_mape:+.1f}%", delta=f"{mejora_mape:.1f}%")
    
    st.markdown("---")
    
    # Gráfico de errores
    st.markdown("### 📉 Evolución de Errores Absolutos")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_analisis['datetime'],
        y=df_analisis['error_abs_ree'],
        mode='lines',
        name='Error REE',
        line=dict(color='#F77F00', width=1.5),
        hovertemplate='<b>REE</b><br>%{x|%d/%m/%Y %H:%M}<br>Error: %{y:,.0f} MW<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_analisis['datetime'],
        y=df_analisis['error_abs_modelo'],
        mode='lines',
        name='Error Modelo',
        line=dict(color='#06A77D', width=1.5),
        hovertemplate='<b>Modelo</b><br>%{x|%d/%m/%Y %H:%M}<br>Error: %{y:,.0f} MW<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Error Absoluto (MW)',
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribución de errores
    st.markdown("### 📊 Distribución de Errores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df_analisis['error_ree'],
            name='REE',
            opacity=0.7,
            marker_color='#F77F00',
            nbinsx=50
        ))
        fig_hist.add_trace(go.Histogram(
            x=df_analisis['error_modelo'],
            name='Modelo',
            opacity=0.7,
            marker_color='#06A77D',
            nbinsx=50
        ))
        fig_hist.update_layout(
            title='Distribución de Errores',
            xaxis_title='Error (MW)',
            yaxis_title='Frecuencia',
            barmode='overlay',
            height=400
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=df_analisis['error_abs_ree'],
            name='REE',
            marker_color='#F77F00'
        ))
        fig_box.add_trace(go.Box(
            y=df_analisis['error_abs_modelo'],
            name='Modelo',
            marker_color='#06A77D'
        ))
        fig_box.update_layout(
            title='Comparación de Errores Absolutos',
            yaxis_title='Error Absoluto (MW)',
            height=400
        )
        st.plotly_chart(fig_box, use_container_width=True)

# ==================== ANÁLISIS TEMPORAL ====================
elif boton_seleccionado == "📈 Análisis Temporal":
    st.title("📈 Análisis Temporal de la Demanda")
    
    # Agregar día de la semana
    df['dia_semana'] = df['datetime'].dt.day_name()
    df['mes'] = df['datetime'].dt.month_name()
    df['hora'] = df['datetime'].dt.hour
    
    # Análisis por día de la semana
    st.markdown("### 📅 Demanda por Día de la Semana")
    
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    demanda_semanal = df.groupby('dia_semana')['demanda_real'].agg(['mean', 'std']).reindex(dias_orden).reset_index()
    demanda_semanal['dia_es'] = dias_es
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=demanda_semanal['dia_es'],
        y=demanda_semanal['mean'],
        error_y=dict(type='data', array=demanda_semanal['std']),
        marker_color='#2E86AB',
        hovertemplate='<b>%{x}</b><br>Promedio: %{y:,.0f} MW<extra></extra>'
    ))
    
    fig.update_layout(
        title='Demanda Promedio por Día de la Semana',
        xaxis_title='Día',
        yaxis_title='Demanda Promedio (MW)',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap por día y hora
    st.markdown("### 🔥 Mapa de Calor: Demanda por Día y Hora")
    
    df_heatmap = df.copy()
    df_heatmap['dia_semana_num'] = df_heatmap['datetime'].dt.dayofweek
    
    pivot_data = df_heatmap.groupby(['dia_semana_num', 'hora'])['demanda_real'].mean().reset_index()
    pivot_table = pivot_data.pivot(index='dia_semana_num', columns='hora', values='demanda_real')
    pivot_table = pivot_table.set_axis(dias_es, axis=0)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='RdYlBu_r',
        hovertemplate='<b>%{y}</b><br>Hora: %{x}<br>Demanda: %{z:,.0f} MW<extra></extra>'
    ))
    
    fig.update_layout(
        title='Patrón Semanal de Demanda',
        xaxis_title='Hora del Día',
        yaxis_title='Día de la Semana',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==================== PRECIO DE LA LUZ ====================
elif boton_seleccionado == "💰 Precio de la Luz":
    st.title("💰 Precio de la Luz - España")
    
    # Cargar datos de precios
    df_precio = cargar_datos_precio()
    
    # Selector de tipo de visualización
    col1, col2, col3 = st.columns([2, 2, 4])
    
    with col1:
        tipo_seleccion = st.radio(
            "Tipo de visualización",
            ["Un día", "Período"],
            horizontal=True,
            key="tipo_precio"
        )
    
    # Selector de fechas según el tipo
    fecha_min = df_precio['fecha'].min()
    fecha_max = df_precio['fecha'].max()
    
    if tipo_seleccion == "Un día":
        with col2:
            fecha_seleccionada = st.date_input(
                "Selecciona un día",
                value=fecha_max,
                min_value=fecha_min,
                max_value=fecha_max,
                key="fecha_precio_unica"
            )
        fecha_inicio = fecha_seleccionada
        fecha_fin = fecha_seleccionada
    else:  # Período
        with col2:
            fecha_inicio = st.date_input(
                "Fecha inicio",
                value=fecha_max - timedelta(days=7),
                min_value=fecha_min,
                max_value=fecha_max,
                key="fecha_precio_inicio"
            )
        
        with col3:
            fecha_fin = st.date_input(
                "Fecha fin",
                value=fecha_max,
                min_value=fecha_inicio,
                max_value=fecha_max,
                key="fecha_precio_fin"
            )
    
    # Filtrar datos
    df_precio_filtrado = df_precio[(df_precio['fecha'] >= fecha_inicio) & (df_precio['fecha'] <= fecha_fin)].copy()
    
    # Métricas principales
    st.markdown("### 📌 Métricas del Período Seleccionado")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        precio_promedio = df_precio_filtrado['precio_real'].mean()
        st.metric("Precio Promedio", f"{precio_promedio:.4f} €/kWh")
    
    with col2:
        precio_maximo = df_precio_filtrado['precio_real'].max()
        hora_maxima = df_precio_filtrado[df_precio_filtrado['precio_real'] == precio_maximo]['datetime'].iloc[0]
        st.metric("Precio Máximo", f"{precio_maximo:.4f} €/kWh")
        st.caption(f"📅 {hora_maxima.strftime('%d/%m/%Y %H:%M')}")
    
    with col3:
        precio_minimo = df_precio_filtrado['precio_real'].min()
        hora_minima = df_precio_filtrado[df_precio_filtrado['precio_real'] == precio_minimo]['datetime'].iloc[0]
        st.metric("Precio Mínimo", f"{precio_minimo:.4f} €/kWh")
        st.caption(f"📅 {hora_minima.strftime('%d/%m/%Y %H:%M')}")
    
    with col4:
        volatilidad = df_precio_filtrado['precio_real'].std()
        st.metric("Volatilidad (σ)", f"{volatilidad:.4f} €/kWh")
    
    st.markdown("---")
    
    # Gráfico principal - Barras para un día, líneas para período
    if tipo_seleccion == "Un día":
        # Gráfico de barras con colores según el precio
        # Colores degradados (verde = bajo, rojo = alto)
        colores = px.colors.diverging.RdYlGn[::-1]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_precio_filtrado['hora'],
            y=df_precio_filtrado['precio_real'],
            marker=dict(
                color=df_precio_filtrado['precio_real'],
                colorscale=colores,
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text="€/kWh",
                        side='right'
                    ),
                    thickness=15,
                    len=0.7
                )
            ),
            name='Precio Real',
            hovertemplate='<b>Hora %{x}:00</b><br>Precio: %{y:.4f} €/kWh<extra></extra>'
        ))
        
        # Línea del precio medio
        precio_medio = df_precio_filtrado['precio_real'].mean()
        fig.add_hline(
            y=precio_medio,
            line_dash="dash",
            line_color="yellow",
            annotation_text=f"Media: {precio_medio:.4f} €/kWh",
            annotation_position="right"
        )
        
        fig.update_layout(
            title=f"Precio de la Luz para Hogares - {fecha_seleccionada.strftime('%d/%m/%Y')}",
            xaxis_title='Hora del Día',
            yaxis_title='Precio (€/kWh)',
            height=500,
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1
            )
        )
    else:
        # Gráfico de líneas para período
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_precio_filtrado['datetime'],
            y=df_precio_filtrado['precio_real'],
            mode='lines',
            name='Precio Real',
            line=dict(color='#FF6B6B', width=2),
            hovertemplate='<b>%{x|%d/%m/%Y %H:%M}</b><br>Precio: %{y:.4f} €/kWh<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Precio de la Luz para Hogares: {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}",
            xaxis_title='Fecha y Hora',
            yaxis_title='Precio (€/kWh)',
            hovermode='x unified',
            height=500
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribución horaria del precio
    st.markdown("### 📊 Distribución Horaria del Precio")
    df_precio_filtrado['hora'] = df_precio_filtrado['datetime'].dt.hour
    precio_horario = df_precio_filtrado.groupby('hora')['precio_real'].agg(['mean', 'min', 'max']).reset_index()
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=precio_horario['hora'],
        y=precio_horario['mean'],
        mode='lines+markers',
        name='Promedio',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=8)
    ))
    
    fig2.add_trace(go.Scatter(
        x=precio_horario['hora'],
        y=precio_horario['max'],
        mode='lines',
        name='Máximo',
        line=dict(color='#FF6B6B', width=1.5, dash='dash'),
        fill=None
    ))
    
    fig2.add_trace(go.Scatter(
        x=precio_horario['hora'],
        y=precio_horario['min'],
        mode='lines',
        name='Mínimo',
        line=dict(color='#95E1D3', width=1.5, dash='dash'),
        fill='tonexty',
        fillcolor='rgba(78, 205, 196, 0.2)'
    ))
    
    fig2.update_layout(
        title='Patrón de Precio por Hora del Día',
        xaxis_title='Hora del Día',
        yaxis_title='Precio (€/kWh)',
        xaxis=dict(tickmode='linear', tick0=0, dtick=2),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# ==================== PREDICCIÓN PRECIO LUZ ====================
elif boton_seleccionado == "💡 Predicción Precio Luz":
    st.title("💡 Predicción de Precio de la Luz")
    
    # Cargar datos de precios
    df_precio = cargar_datos_precio()
    
    # Filtrar solo datos con predicciones (desde 2025-09-21)
    df_pred = df_precio[df_precio['precio_predicho'].notna()].copy()
    
    # Selector de tipo de visualización
    col1, col2, col3 = st.columns([2, 2, 4])
    
    with col1:
        tipo_seleccion = st.radio(
            "Tipo de visualización",
            ["Un día", "Período"],
            horizontal=True,
            key="tipo_pred_luz"
        )
    
    # Selector de fechas según el tipo
    fecha_min = df_pred['fecha'].min()
    fecha_max = df_pred['fecha'].max()
    
    if tipo_seleccion == "Un día":
        with col2:
            fecha_seleccionada = st.date_input(
                "Selecciona un día",
                value=fecha_max,
                min_value=fecha_min,
                max_value=fecha_max,
                key="fecha_pred_unica"
            )
        fecha_inicio = fecha_seleccionada
        fecha_fin = fecha_seleccionada
    else:  # Período
        with col2:
            fecha_inicio = st.date_input(
                "Fecha inicio",
                value=fecha_min,
                min_value=fecha_min,
                max_value=fecha_max,
                key="fecha_pred_inicio"
            )
        
        with col3:
            fecha_fin = st.date_input(
                "Fecha fin",
                value=fecha_max,
                min_value=fecha_inicio,
                max_value=fecha_max,
                key="fecha_pred_fin"
            )
    
    # Filtrar datos
    df_pred_filtrado = df_pred[(df_pred['fecha'] >= fecha_inicio) & (df_pred['fecha'] <= fecha_fin)].copy()
    
    # Calcular métricas de error
    df_pred_filtrado['error'] = df_pred_filtrado['precio_real'] - df_pred_filtrado['precio_predicho']
    df_pred_filtrado['error_abs'] = np.abs(df_pred_filtrado['error'])
    df_pred_filtrado['error_pct'] = (df_pred_filtrado['error_abs'] / df_pred_filtrado['precio_real']) * 100
    
    # Métricas principales
    st.markdown("### 📊 Métricas de Precisión del Modelo")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        mae = df_pred_filtrado['error_abs'].mean()
        st.metric("MAE", f"{mae:.4f} €/kWh")
    
    with col2:
        rmse = np.sqrt((df_pred_filtrado['error']**2).mean())
        st.metric("RMSE", f"{rmse:.4f} €/kWh")
    
    with col3:
        mape = df_pred_filtrado['error_pct'].mean()
        st.metric("MAPE", f"{mape:.2f}%")
    
    with col4:
        r2 = 1 - (np.sum(df_pred_filtrado['error']**2) / np.sum((df_pred_filtrado['precio_real'] - df_pred_filtrado['precio_real'].mean())**2))
        st.metric("R² Score", f"{r2:.4f}")
    
    st.markdown("---")
    
    # Gráfico comparativo
    st.markdown("### 📈 Comparación: Precio Real vs Predicho")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_pred_filtrado['datetime'],
        y=df_pred_filtrado['precio_real'],
        mode='lines',
        name='Precio Real',
        line=dict(color='#2E86AB', width=2),
        hovertemplate='<b>Real</b><br>%{x|%d/%m/%Y %H:%M}<br>%{y:.4f} €/kWh<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_pred_filtrado['datetime'],
        y=df_pred_filtrado['precio_predicho'],
        mode='lines',
        name='Precio Predicho',
        line=dict(color='#F77F00', width=1.5, dash='dash'),
        hovertemplate='<b>Predicho</b><br>%{x|%d/%m/%Y %H:%M}<br>%{y:.4f} €/kWh<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Predicción de Precios para Hogares: {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}",
        xaxis_title='Fecha y Hora',
        yaxis_title='Precio (€/kWh)',
        hovermode='x unified',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de errores
    st.markdown("### 📉 Evolución del Error de Predicción")
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=df_pred_filtrado['datetime'],
        y=df_pred_filtrado['error'],
        mode='lines',
        name='Error',
        line=dict(color='#E63946', width=1.5),
        fill='tozeroy',
        fillcolor='rgba(230, 57, 70, 0.2)',
        hovertemplate='<b>Error</b><br>%{x|%d/%m/%Y %H:%M}<br>%{y:.4f} €/kWh<extra></extra>'
    ))
    
    fig2.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig2.update_layout(
        title='Error de Predicción a lo largo del tiempo',
        xaxis_title='Fecha y Hora',
        yaxis_title='Error (€/kWh)',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Distribución de errores
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Distribución de Errores")
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df_pred_filtrado['error'],
            nbinsx=50,
            marker_color='#4ECDC4',
            opacity=0.7,
            name='Error'
        ))
        fig_hist.update_layout(
            title='Histograma de Errores',
            xaxis_title='Error (€/kWh)',
            yaxis_title='Frecuencia',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Errores Absolutos")
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=df_pred_filtrado['error_abs'],
            marker_color='#F77F00',
            name='Error Absoluto'
        ))
        fig_box.update_layout(
            title='Box Plot de Errores Absolutos',
            yaxis_title='Error Absoluto (€/kWh)',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Scatter plot: Real vs Predicho
    st.markdown("### 🎯 Dispersión: Real vs Predicho")
    
    fig_scatter = go.Figure()
    
    fig_scatter.add_trace(go.Scatter(
        x=df_pred_filtrado['precio_real'],
        y=df_pred_filtrado['precio_predicho'],
        mode='markers',
        marker=dict(
            color=df_pred_filtrado['error_abs'],
            colorscale='Reds',
            size=5,
            showscale=True,
            colorbar=dict(title="Error Abs")
        ),
        name='Predicciones',
        hovertemplate='<b>Real:</b> %{x:.4f} €/kWh<br><b>Predicho:</b> %{y:.4f} €/kWh<extra></extra>'
    ))
    
    # Línea de predicción perfecta
    min_val = min(df_pred_filtrado['precio_real'].min(), df_pred_filtrado['precio_predicho'].min())
    max_val = max(df_pred_filtrado['precio_real'].max(), df_pred_filtrado['precio_predicho'].max())
    
    fig_scatter.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(color='gray', dash='dash'),
        name='Predicción Perfecta',
        hoverinfo='skip'
    ))
    
    fig_scatter.update_layout(
        title='Precio Real vs Precio Predicho para Hogares',
        xaxis_title='Precio Real (€/kWh)',
        yaxis_title='Precio Predicho (€/kWh)',
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)