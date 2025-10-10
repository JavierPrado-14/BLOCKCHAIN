#!/usr/bin/env python3
"""
Dashboard con IA para Blockchain Corda
Dashboard interactivo con análisis avanzados y capacidades de IA
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
import numpy as np
from datetime import datetime, timedelta
import json
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import google.generativeai as genai
import time
import threading
import queue
import warnings
warnings.filterwarnings('ignore')

# ===== Configuración de Gemini =====
GEMINI_API_KEY = "AIzaSyBM5jwwPLcn9aldmaypSP-ywvqecVfJEIA"
genai.configure(api_key=GEMINI_API_KEY)

# Configuración de la página
st.set_page_config(
    page_title="Corda Blockchain Dashboard",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para el dashboard
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .ai-section {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

class CordaDashboard:
    """Dashboard principal para análisis de datos de Corda"""
    
    def __init__(self):
        """Inicializar el dashboard"""
        self.db_config = {
            'host': 'dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com',
            'port': 5432,
            'database': 'blokchain_bd',
            'user': 'blokchain_bd_user',
            'password': 'RlxkDsSrWcte8ASrxsztagJWod7qNrWP'
        }
        self.data = None
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.load_data()
    
    def load_data(self, time_filter=None, limit=None):
        """Cargar datos desde PostgreSQL con filtros dinámicos"""
        try:
            conn = psycopg2.connect(**self.db_config)
            
            # Construir query dinámico
            base_query = """
            SELECT 
                id, timestamp, state_type, participants, amount, currency, 
                status, block_height, network, notary, contract, flow_id,
                extraction_timestamp, processed, processing_timestamp
            FROM corda_transactions
            """
            
            where_conditions = []
            params = []
            
            # Filtro de tiempo dinámico
            if time_filter:
                if time_filter == "last_hour":
                    where_conditions.append("timestamp >= NOW() - INTERVAL '1 hour'")
                elif time_filter == "last_24h":
                    where_conditions.append("timestamp >= NOW() - INTERVAL '24 hours'")
                elif time_filter == "last_7d":
                    where_conditions.append("timestamp >= NOW() - INTERVAL '7 days'")
                elif time_filter == "last_30d":
                    where_conditions.append("timestamp >= NOW() - INTERVAL '30 days'")
                elif time_filter == "real_time":
                    # Solo transacciones de los últimos 5 minutos para análisis en tiempo real
                    where_conditions.append("timestamp >= NOW() - INTERVAL '5 minutes'")
            
            # Agregar condiciones WHERE si existen
            if where_conditions:
                base_query += " WHERE " + " AND ".join(where_conditions)
            
            # Ordenar por timestamp descendente
            base_query += " ORDER BY timestamp DESC"
            
            # Agregar LIMIT si se especifica
            if limit:
                base_query += f" LIMIT {limit}"
            
            # Ejecutar query
            self.data = pd.read_sql_query(base_query, conn)
            conn.close()
            
            if not self.data.empty:
                # Procesar datos
                self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
                self.data['amount_numeric'] = pd.to_numeric(self.data['amount'], errors='coerce')
                self.data['date'] = self.data['timestamp'].dt.date
                self.data['hour'] = self.data['timestamp'].dt.hour
                self.data['day_of_week'] = self.data['timestamp'].dt.day_name()
                self.data['minute'] = self.data['timestamp'].dt.minute
                
                # Agregar timestamp de carga
                self.data['loaded_at'] = datetime.now()
            
        except Exception as e:
            st.error(f"Error cargando datos: {str(e)}")
            self.data = pd.DataFrame()
    
    def get_realtime_stats(self):
        """Obtener estadísticas en tiempo real"""
        try:
            conn = psycopg2.connect(**self.db_config)
            
            # Query para estadísticas en tiempo real
            stats_query = """
            SELECT 
                COUNT(*) as total_transactions,
                COUNT(CASE WHEN timestamp >= NOW() - INTERVAL '1 hour' THEN 1 END) as last_hour,
                COUNT(CASE WHEN timestamp >= NOW() - INTERVAL '24 hours' THEN 1 END) as last_24h,
                COALESCE(SUM(CASE WHEN timestamp >= NOW() - INTERVAL '24 hours' THEN amount::numeric END), 0) as total_amount_24h,
                COALESCE(AVG(CASE WHEN timestamp >= NOW() - INTERVAL '24 hours' THEN amount::numeric END), 0) as avg_amount_24h,
                MAX(timestamp) as last_transaction
            FROM corda_transactions
            """
            
            stats = pd.read_sql_query(stats_query, conn)
            conn.close()
            
            return stats.iloc[0].to_dict()
            
        except Exception as e:
            st.error(f"Error obteniendo estadísticas: {str(e)}")
            return {}
    
    def render_header(self):
        """Renderizar encabezado del dashboard"""
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown('<h1 class="main-header">🔗 Corda Blockchain Dashboard</h1>', unsafe_allow_html=True)
            st.markdown("### Análisis en Tiempo Real con Inteligencia Artificial")
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Actualizar Datos", use_container_width=True, type="primary"):
                with st.spinner("Actualizando datos..."):
                    # Cargar datos sin filtro de tiempo para obtener todos los datos
                    self.load_data()
                    st.rerun()
        
        # Estadísticas en tiempo real
        realtime_stats = self.get_realtime_stats()
        
        if realtime_stats:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "📊 Total Transacciones",
                    f"{realtime_stats.get('total_transactions', 0):,}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "⏰ Última Hora",
                    f"{realtime_stats.get('last_hour', 0):,}",
                    delta=None
                )
            
            with col3:
                st.metric(
                    "📈 Últimas 24h",
                    f"{realtime_stats.get('last_24h', 0):,}",
                    delta=None
                )
            
            with col4:
                last_tx = realtime_stats.get('last_transaction', 'N/A')
                if last_tx != 'N/A':
                    last_tx = pd.to_datetime(last_tx)
                    time_diff = datetime.now() - last_tx
                    if time_diff.total_seconds() < 60:
                        status = "🟢 Activo"
                    elif time_diff.total_seconds() < 300:
                        status = "🟡 Reciente"
                    else:
                        status = "🔴 Inactivo"
                else:
                    status = "❌ Sin datos"
                
                st.metric(
                    "🔄 Estado",
                    status,
                    delta=None
                )
            
            st.info(f"💡 Última transacción: {realtime_stats.get('last_transaction', 'N/A')}")
        
        if not self.data.empty:
            st.success(f"✅ {len(self.data)} transacciones cargadas - Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.error("❌ No se pudieron cargar los datos")
    
    def render_metrics(self):
        """Renderizar métricas principales"""
        if self.data.empty:
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_amount = self.data['amount_numeric'].sum()
            st.metric(
                "💰 Monto Total",
                f"${total_amount:,.2f}",
                delta=None
            )
        
        with col2:
            avg_amount = self.data['amount_numeric'].mean()
            st.metric(
                "📊 Monto Promedio",
                f"${avg_amount:,.2f}",
                delta=None
            )
        
        with col3:
            total_transactions = len(self.data)
            st.metric(
                "📈 Total Transacciones",
                f"{total_transactions:,}",
                delta=None
            )
        
        with col4:
            unique_currencies = self.data['currency'].nunique()
            st.metric(
                "💱 Monedas",
                f"{unique_currencies}",
                delta=None
            )
    
    def render_time_series_analysis(self):
        """Análisis de series temporales"""
        st.header("📈 Análisis de Series Temporales")
        
        if self.data.empty:
            return
        
        # Agrupar por fecha
        daily_data = self.data.groupby('date').agg({
            'amount_numeric': ['sum', 'count', 'mean'],
            'id': 'count'
        }).round(2)
        
        daily_data.columns = ['Total_Amount', 'Transaction_Count', 'Avg_Amount', 'Total_Transactions']
        daily_data = daily_data.reset_index()
        
        # Gráfico de evolución temporal
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Evolución del Monto Total', 'Número de Transacciones', 
                          'Monto Promedio por Día', 'Distribución por Hora'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Monto total por día
        fig.add_trace(
            go.Scatter(x=daily_data['date'], y=daily_data['Total_Amount'], 
                      name='Monto Total', line=dict(color='#1f77b4')),
            row=1, col=1
        )
        
        # Número de transacciones por día
        fig.add_trace(
            go.Scatter(x=daily_data['date'], y=daily_data['Transaction_Count'], 
                      name='Transacciones', line=dict(color='#ff7f0e')),
            row=1, col=2
        )
        
        # Monto promedio por día
        fig.add_trace(
            go.Scatter(x=daily_data['date'], y=daily_data['Avg_Amount'], 
                      name='Monto Promedio', line=dict(color='#2ca02c')),
            row=2, col=1
        )
        
        # Distribución por hora
        hourly_dist = self.data.groupby('hour').size()
        fig.add_trace(
            go.Bar(x=hourly_dist.index, y=hourly_dist.values, 
                   name='Por Hora', marker_color='#d62728'),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=True, title_text="Análisis Temporal de Transacciones")
        st.plotly_chart(fig, use_container_width=True)
    
    def generate_gemini_insights(self):
        """Generar insights usando Gemini AI con análisis dinámico"""
        if self.data.empty:
            return None
        
        try:
            # Determinar el contexto temporal de los datos
            time_range = self.data['timestamp'].max() - self.data['timestamp'].min()
            hours_range = time_range.total_seconds() / 3600
            
            # Contexto temporal
            if hours_range < 1:
                time_context = "últimos minutos (análisis en tiempo real)"
            elif hours_range < 24:
                time_context = f"últimas {hours_range:.1f} horas"
            elif hours_range < 168:  # 7 días
                time_context = f"últimos {hours_range/24:.1f} días"
            else:
                time_context = f"últimos {hours_range/24:.0f} días"
            
            # Estadísticas dinámicas
            latest_tx = self.data['timestamp'].max()
            oldest_tx = self.data['timestamp'].min()
            time_since_latest = datetime.now() - latest_tx
            
            # Preparar resumen dinámico para Gemini
            summary = f"""
Analiza los siguientes datos de transacciones de blockchain Corda de los {time_context} y proporciona insights valiosos:

CONTEXTO TEMPORAL:
- Período analizado: {time_context}
- Última transacción: {latest_tx}
- Tiempo desde última transacción: {time_since_latest.total_seconds():.0f} segundos
- Rango completo: {oldest_tx} a {latest_tx}

ESTADÍSTICAS ACTUALES:
- Total de transacciones: {len(self.data)}
- Monto total: ${self.data['amount_numeric'].sum():,.2f}
- Monto promedio: ${self.data['amount_numeric'].mean():,.2f}
- Monto máximo: ${self.data['amount_numeric'].max():,.2f}
- Monto mínimo: ${self.data['amount_numeric'].min():,.2f}

DISTRIBUCIÓN POR MONEDA:
{self.data['currency'].value_counts().to_dict()}

DISTRIBUCIÓN POR ESTADO:
{self.data['status'].value_counts().to_dict()}

DISTRIBUCIÓN POR TIPO DE ESTADO:
{self.data['state_type'].value_counts().to_dict()}

PATRONES TEMPORALES ESPECÍFICOS:
- Transacciones por hora: {self.data.groupby('hour').size().to_dict()}
- Transacciones por día: {self.data.groupby('date').size().to_dict()}
- Horas más activas: {self.data.groupby('hour').size().nlargest(3).to_dict()}
- Días más activos: {self.data.groupby('day_of_week').size().nlargest(3).to_dict()}

ACTIVIDAD RECIENTE:
- Transacciones en última hora: {len(self.data[self.data['timestamp'] >= latest_tx - timedelta(hours=1)])}
- Transacciones en últimos 10 minutos: {len(self.data[self.data['timestamp'] >= latest_tx - timedelta(minutes=10)])}

Por favor proporciona un análisis específico para este período temporal:
1. **Análisis de actividad actual**: ¿Qué tan activo está el sistema ahora?
2. **Patrones identificados**: ¿Qué patrones únicos ves en este período?
3. **Tendencias temporales**: ¿Cómo ha cambiado la actividad en este tiempo?
4. **Anomalías detectadas**: ¿Hay comportamientos inusuales o transacciones sospechosas?
5. **Recomendaciones inmediatas**: ¿Qué acciones se deberían tomar basadas en estos datos?
6. **Predicciones a corto plazo**: ¿Qué esperas que pase en las próximas horas?

Responde en español, enfócate en la relevancia temporal y proporciona insights accionables.
"""
            
            # Generar respuesta con Gemini
            response = self.model.generate_content(summary)
            return response.text
            
        except Exception as e:
            st.error(f"Error al generar insights con Gemini: {str(e)}")
            return None
    
    def render_gemini_insights(self):
        """Renderizar insights generados por Gemini AI"""
        st.header("🧠 Insights Generados por IA (Gemini)")
        
        if self.data.empty:
            st.warning("No hay datos disponibles para análisis")
            return
        
        # Mostrar contexto temporal de los datos
        if not self.data.empty:
            latest_tx = self.data['timestamp'].max()
            oldest_tx = self.data['timestamp'].min()
            time_range = latest_tx - oldest_tx
            time_since_latest = datetime.now() - latest_tx
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Transacciones Analizadas", len(self.data))
            with col2:
                st.metric("⏰ Rango Temporal", f"{time_range.days}d {time_range.seconds//3600}h")
            with col3:
                st.metric("🕐 Última Actividad", f"{time_since_latest.total_seconds():.0f}s")
        
        col1, col2 = st.columns([4, 1])
        
        with col2:
            generate_button = st.button("✨ Generar Análisis IA", use_container_width=True, type="primary")
            
            # Botón para regenerar con datos actualizados
            if 'gemini_insights' in st.session_state:
                regenerate_button = st.button("🔄 Regenerar Análisis", use_container_width=True)
                if regenerate_button:
                    # Limpiar insights anteriores
                    if 'gemini_insights' in st.session_state:
                        del st.session_state.gemini_insights
        
        # Generar insights si se solicita o si no existen
        if generate_button or 'gemini_insights' not in st.session_state:
            with st.spinner("🤖 Gemini AI está analizando los datos en tiempo real..."):
                insights = self.generate_gemini_insights()
                if insights:
                    st.session_state.gemini_insights = insights
                    st.session_state.gemini_generated_at = datetime.now()
        
        # Mostrar insights si existen
        if 'gemini_insights' in st.session_state:
            st.markdown('<div class="ai-section">', unsafe_allow_html=True)
            
            # Header con información del análisis
            generated_at = st.session_state.get('gemini_generated_at', datetime.now())
            st.markdown(f"### 📊 Análisis Inteligente - {generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Mostrar insights
            st.markdown(st.session_state.gemini_insights)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Información adicional
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"🕐 Análisis generado: {generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            with col2:
                st.caption(f"📊 Basado en {len(self.data)} transacciones")
                
            # Botón para limpiar cache
            if st.button("🗑️ Limpiar Análisis", help="Elimina el análisis actual para generar uno nuevo"):
                if 'gemini_insights' in st.session_state:
                    del st.session_state.gemini_insights
                if 'gemini_generated_at' in st.session_state:
                    del st.session_state.gemini_generated_at
                st.rerun()
        else:
            st.info("👆 Haz clic en 'Generar Análisis IA' para obtener insights inteligentes sobre tus datos")
    
    def render_ai_analysis(self):
        """Análisis con Inteligencia Artificial"""
        st.header("🤖 Análisis con Machine Learning")
        
        if self.data.empty:
            return
        
        # Preparar datos para ML
        ml_data = self.data[['amount_numeric', 'hour', 'day_of_week']].copy()
        ml_data['day_of_week_num'] = pd.Categorical(ml_data['day_of_week']).codes
        ml_data = ml_data.dropna()
        
        if len(ml_data) < 10:
            st.warning("No hay suficientes datos para análisis de IA")
            return
        
        # Análisis de anomalías
        st.subheader("🔍 Detección de Anomalías")
        
        # Preparar características
        features = ml_data[['amount_numeric', 'hour', 'day_of_week_num']]
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # Detectar anomalías
        isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        anomaly_labels = isolation_forest.fit_predict(features_scaled)
        
        # Agregar etiquetas a los datos
        ml_data['anomaly'] = anomaly_labels
        anomalies = ml_data[ml_data['anomaly'] == -1]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🚨 Anomalías Detectadas", f"{len(anomalies)}")
        
        with col2:
            anomaly_rate = len(anomalies) / len(ml_data) * 100
            st.metric("📊 Tasa de Anomalías", f"{anomaly_rate:.1f}%")
        
        # Visualizar anomalías
        fig_anomalies = px.scatter(
            ml_data, x='amount_numeric', y='hour',
            color='anomaly', 
            title='Detección de Anomalías en Transacciones',
            labels={'amount_numeric': 'Monto', 'hour': 'Hora del Día'},
            color_discrete_map={1: 'blue', -1: 'red'}
        )
        st.plotly_chart(fig_anomalies, use_container_width=True)
        
        # Clustering
        st.subheader("🎯 Análisis de Clusters")
        
        # Aplicar K-means
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(features_scaled)
        ml_data['cluster'] = clusters
        
        # Visualizar clusters
        fig_clusters = px.scatter_3d(
            ml_data, x='amount_numeric', y='hour', z='day_of_week_num',
            color='cluster',
            title='Clustering de Transacciones',
            labels={'amount_numeric': 'Monto', 'hour': 'Hora', 'day_of_week_num': 'Día de la Semana'}
        )
        st.plotly_chart(fig_clusters, use_container_width=True)
        
        # Mostrar detalles de anomalías
        if len(anomalies) > 0:
            st.subheader("📋 Detalles de Anomalías Detectadas")
            anomaly_details = self.data[self.data.index.isin(anomalies.index)]
            st.dataframe(anomaly_details[['id', 'timestamp', 'amount', 'currency', 'state_type', 'status']])
    
    def render_currency_analysis(self):
        """Análisis por moneda"""
        st.header("💱 Análisis por Moneda")
        
        if self.data.empty:
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución por moneda
            currency_dist = self.data['currency'].value_counts()
            fig_currency = px.pie(
                values=currency_dist.values, 
                names=currency_dist.index,
                title="Distribución por Moneda"
            )
            st.plotly_chart(fig_currency, use_container_width=True)
        
        with col2:
            # Monto total por moneda
            currency_amount = self.data.groupby('currency')['amount_numeric'].sum().sort_values(ascending=False)
            fig_amount = px.bar(
                x=currency_amount.index, 
                y=currency_amount.values,
                title="Monto Total por Moneda",
                labels={'x': 'Moneda', 'y': 'Monto Total'}
            )
            st.plotly_chart(fig_amount, use_container_width=True)
    
    def render_state_analysis(self):
        """Análisis por tipo de estado"""
        st.header("🏛️ Análisis por Tipo de Estado")
        
        if self.data.empty:
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución por tipo de estado
            state_dist = self.data['state_type'].value_counts()
            fig_state = px.bar(
                x=state_dist.index, 
                y=state_dist.values,
                title="Distribución por Tipo de Estado",
                labels={'x': 'Tipo de Estado', 'y': 'Número de Transacciones'}
            )
            fig_state.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_state, use_container_width=True)
        
        with col2:
            # Monto promedio por tipo de estado
            state_amount = self.data.groupby('state_type')['amount_numeric'].mean().sort_values(ascending=False)
            fig_state_amount = px.bar(
                x=state_amount.index, 
                y=state_amount.values,
                title="Monto Promedio por Tipo de Estado",
                labels={'x': 'Tipo de Estado', 'y': 'Monto Promedio'}
            )
            fig_state_amount.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_state_amount, use_container_width=True)
    
    def render_status_analysis(self):
        """Análisis por estado de transacción"""
        st.header("📊 Análisis por Estado de Transacción")
        
        if self.data.empty:
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución por estado
            status_dist = self.data['status'].value_counts()
            fig_status = px.pie(
                values=status_dist.values, 
                names=status_dist.index,
                title="Distribución por Estado"
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Tasa de éxito por tipo de estado
            success_rate = self.data.groupby('state_type')['status'].apply(
                lambda x: (x == 'CONFIRMED').sum() / len(x) * 100
            ).sort_values(ascending=False)
            
            fig_success = px.bar(
                x=success_rate.index, 
                y=success_rate.values,
                title="Tasa de Éxito por Tipo de Estado (%)",
                labels={'x': 'Tipo de Estado', 'y': 'Tasa de Éxito (%)'}
            )
            fig_success.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_success, use_container_width=True)
    
    def render_realtime_controls(self):
        """Controles de tiempo real"""
        st.sidebar.header("⏰ Controles de Tiempo Real")
        
        # Selector de modo de análisis
        analysis_mode = st.sidebar.selectbox(
            "🎯 Modo de Análisis",
            options=[
                "📊 Todos los Datos",
                "⏰ Última Hora",
                "📈 Últimas 24 Horas", 
                "📅 Últimos 7 Días",
                "🗓️ Últimos 30 Días",
                "🔥 Tiempo Real (5 min)"
            ],
            index=0
        )
        
        # Mapear opciones a filtros
        time_filters = {
            "📊 Todos los Datos": None,
            "⏰ Última Hora": "last_hour",
            "📈 Últimas 24 Horas": "last_24h",
            "📅 Últimos 7 Días": "last_7d",
            "🗓️ Últimos 30 Días": "last_30d",
            "🔥 Tiempo Real (5 min)": "real_time"
        }
        
        selected_filter = time_filters[analysis_mode]
        
        # Auto-refresh toggle
        auto_refresh = st.sidebar.checkbox("🔄 Auto-actualización", value=False)
        
        if auto_refresh:
            refresh_interval = st.sidebar.slider(
                "⏱️ Intervalo (segundos)",
                min_value=10,
                max_value=300,
                value=60,
                step=10
            )
            
            # Mostrar countdown
            if 'last_refresh' not in st.session_state:
                st.session_state.last_refresh = time.time()
            
            time_since_refresh = time.time() - st.session_state.last_refresh
            time_until_next = refresh_interval - time_since_refresh
            
            if time_until_next > 0:
                st.sidebar.info(f"🕐 Próxima actualización en: {int(time_until_next)}s")
            else:
                st.sidebar.success("🔄 Actualizando automáticamente...")
                st.session_state.last_refresh = time.time()
                # Recargar datos con filtro seleccionado
                self.load_data(time_filter=selected_filter)
                st.rerun()
        
        # Botón para aplicar filtro manualmente
        if st.sidebar.button("🎯 Aplicar Filtro", use_container_width=True):
            with st.spinner(f"Cargando datos: {analysis_mode}..."):
                self.load_data(time_filter=selected_filter)
                st.rerun()
        
        return selected_filter
    
    def render_interactive_filters(self):
        """Filtros interactivos"""
        st.sidebar.header("🔧 Filtros Interactivos")
        
        if self.data.empty:
            return
        
        # Filtro por fecha
        date_range = st.sidebar.date_input(
            "Rango de Fechas",
            value=(self.data['date'].min(), self.data['date'].max()),
            min_value=self.data['date'].min(),
            max_value=self.data['date'].max()
        )
        
        # Filtro por moneda
        currencies = st.sidebar.multiselect(
            "Monedas",
            options=self.data['currency'].unique(),
            default=self.data['currency'].unique()
        )
        
        # Filtro por tipo de estado
        state_types = st.sidebar.multiselect(
            "Tipos de Estado",
            options=self.data['state_type'].unique(),
            default=self.data['state_type'].unique()
        )
        
        # Filtro por estado de transacción
        statuses = st.sidebar.multiselect(
            "Estados de Transacción",
            options=self.data['status'].unique(),
            default=self.data['status'].unique()
        )
        
        # Filtro por rango de monto
        amount_range = st.sidebar.slider(
            "Rango de Monto",
            min_value=float(self.data['amount_numeric'].min()),
            max_value=float(self.data['amount_numeric'].max()),
            value=(float(self.data['amount_numeric'].min()), float(self.data['amount_numeric'].max()))
        )
        
        # Aplicar filtros
        filtered_data = self.data[
            (self.data['date'] >= date_range[0]) & 
            (self.data['date'] <= date_range[1]) &
            (self.data['currency'].isin(currencies)) &
            (self.data['state_type'].isin(state_types)) &
            (self.data['status'].isin(statuses)) &
            (self.data['amount_numeric'] >= amount_range[0]) &
            (self.data['amount_numeric'] <= amount_range[1])
        ]
        
        st.sidebar.metric("Transacciones Filtradas", len(filtered_data))
        
        return filtered_data
    
    def render_export_options(self):
        """Opciones de exportación"""
        st.sidebar.header("📤 Exportar Datos")
        
        if self.data.empty:
            return
        
        # Exportar a CSV
        csv = self.data.to_csv(index=False)
        st.sidebar.download_button(
            label="📊 Descargar CSV",
            data=csv,
            file_name=f"corda_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Exportar a JSON
        json_data = self.data.to_json(orient='records', date_format='iso')
        st.sidebar.download_button(
            label="📄 Descargar JSON",
            data=json_data,
            file_name=f"corda_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    def run(self):
        """Ejecutar el dashboard completo"""
        # Renderizar encabezado con estadísticas en tiempo real
        self.render_header()
        
        # Renderizar controles de tiempo real
        selected_time_filter = self.render_realtime_controls()
        
        # Renderizar métricas principales
        self.render_metrics()
        
        # Renderizar filtros interactivos
        filtered_data = self.render_interactive_filters()
        
        # Renderizar opciones de exportación
        self.render_export_options()
        
        # Renderizar análisis
        if not filtered_data.empty:
            # Sección de IA Generativa con Gemini (primera)
            self.render_gemini_insights()
            
            st.markdown("---")
            
            # Análisis tradicionales
            self.render_time_series_analysis()
            self.render_currency_analysis()
            self.render_state_analysis()
            self.render_status_analysis()
            
            # Análisis de Machine Learning
            self.render_ai_analysis()
        else:
            st.warning("No hay datos que coincidan con los filtros seleccionados")
            
            # Si no hay datos filtrados pero hay datos en general, mostrar mensaje
            if not self.data.empty:
                st.info("💡 Prueba cambiar los filtros o seleccionar un rango de tiempo diferente")
            else:
                st.error("❌ No hay datos disponibles. Verifica la conexión a la base de datos.")

def main():
    """Función principal"""
    dashboard = CordaDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
