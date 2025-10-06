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
import warnings
warnings.filterwarnings('ignore')

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
        self.load_data()
    
    def load_data(self):
        """Cargar datos desde PostgreSQL"""
        try:
            conn = psycopg2.connect(**self.db_config)
            query = """
            SELECT 
                id, timestamp, state_type, participants, amount, currency, 
                status, block_height, network, notary, contract, flow_id,
                extraction_timestamp, processed, processing_timestamp
            FROM corda_transactions
            ORDER BY timestamp DESC
            """
            self.data = pd.read_sql_query(query, conn)
            conn.close()
            
            # Procesar datos
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
            self.data['amount_numeric'] = pd.to_numeric(self.data['amount'], errors='coerce')
            self.data['date'] = self.data['timestamp'].dt.date
            self.data['hour'] = self.data['timestamp'].dt.hour
            self.data['day_of_week'] = self.data['timestamp'].dt.day_name()
            
        except Exception as e:
            st.error(f"Error cargando datos: {str(e)}")
            self.data = pd.DataFrame()
    
    def render_header(self):
        """Renderizar encabezado del dashboard"""
        st.markdown('<h1 class="main-header">🔗 Corda Blockchain Dashboard</h1>', unsafe_allow_html=True)
        st.markdown("### Análisis Avanzado con Inteligencia Artificial")
        
        if not self.data.empty:
            st.success(f"✅ Conectado a PostgreSQL - {len(self.data)} transacciones cargadas")
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
    
    def render_ai_analysis(self):
        """Análisis con Inteligencia Artificial"""
        st.header("🤖 Análisis con Inteligencia Artificial")
        
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
        # Renderizar encabezado
        self.render_header()
        
        # Renderizar métricas principales
        self.render_metrics()
        
        # Renderizar filtros interactivos
        filtered_data = self.render_interactive_filters()
        
        # Renderizar opciones de exportación
        self.render_export_options()
        
        # Renderizar análisis
        if not filtered_data.empty:
            self.render_time_series_analysis()
            self.render_currency_analysis()
            self.render_state_analysis()
            self.render_status_analysis()
            self.render_ai_analysis()
        else:
            st.warning("No hay datos que coincidan con los filtros seleccionados")

def main():
    """Función principal"""
    dashboard = CordaDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
