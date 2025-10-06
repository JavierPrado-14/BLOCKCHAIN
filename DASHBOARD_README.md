# 🔗 Corda Blockchain Dashboard con IA

## 🎯 Descripción
Dashboard interactivo y moderno para análisis avanzado de datos de blockchain Corda con capacidades de Inteligencia Artificial.

## ✨ Características Principales

### 📊 Visualizaciones Avanzadas
- **Análisis Temporal**: Series de tiempo con evolución de transacciones
- **Análisis por Moneda**: Distribución y montos por divisa
- **Análisis por Estado**: Tipos de transacciones y contratos
- **Análisis de Status**: Estados de confirmación y tasas de éxito

### 🤖 Inteligencia Artificial
- **Detección de Anomalías**: Identificación automática de transacciones inusuales
- **Clustering**: Agrupación de transacciones por patrones similares
- **Análisis Predictivo**: Tendencias y patrones en los datos
- **Machine Learning**: Modelos de clasificación y regresión

### 🔧 Funcionalidades Interactivas
- **Filtros Dinámicos**: Por fecha, moneda, tipo de estado, status
- **Rangos de Monto**: Sliders para filtrar por valor
- **Exportación**: Descarga de datos en CSV y JSON
- **Tiempo Real**: Actualización automática de métricas

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.8+
- PostgreSQL (base de datos en Render)
- Dependencias instaladas

### Instalación
```bash
# Instalar dependencias
pip install -r requirements.txt

# Verificar configuración
python test_dashboard.py
```

### Ejecución
```bash
# Ejecutar dashboard
streamlit run corda_dashboard.py
```

El dashboard estará disponible en: **http://localhost:8501**

## 📈 Métricas Disponibles

### Métricas Principales
- **💰 Monto Total**: Suma de todas las transacciones
- **📊 Monto Promedio**: Valor promedio por transacción
- **📈 Total Transacciones**: Número total de registros
- **💱 Monedas**: Número de divisas diferentes

### Análisis Temporal
- Evolución del monto total por día
- Número de transacciones por día
- Monto promedio por día
- Distribución por hora del día

### Análisis por Categorías
- **Distribución por Moneda**: USD, EUR, GBP, JPY, CHF, CAD, AUD
- **Tipos de Estado**: LoanState, AssetState, CommercialPaperState, etc.
- **Estados de Transacción**: CONFIRMED, PENDING, FAILED
- **Tasas de Éxito**: Porcentaje de transacciones confirmadas

## 🤖 Capacidades de IA

### Detección de Anomalías
- **Algoritmo**: Isolation Forest
- **Contaminación**: 10% (configurable)
- **Características**: Monto, hora, día de la semana
- **Visualización**: Scatter plot con anomalías marcadas

### Clustering
- **Algoritmo**: K-Means
- **Clusters**: 3 grupos automáticos
- **Visualización**: Gráfico 3D interactivo
- **Características**: Monto, hora, día de la semana

### Análisis Predictivo
- **Tendencias**: Patrones temporales
- **Correlaciones**: Relaciones entre variables
- **Predicciones**: Estimaciones futuras
- **Alertas**: Notificaciones automáticas

## 🔧 Configuración

### Base de Datos
- **Host**: dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com
- **Puerto**: 5432
- **Base de datos**: blokchain_bd
- **Tabla**: corda_transactions

### Filtros Disponibles
- **Rango de Fechas**: Selector de fechas
- **Monedas**: Multi-selector
- **Tipos de Estado**: Multi-selector
- **Estados de Transacción**: Multi-selector
- **Rango de Monto**: Slider numérico

## 📊 Visualizaciones

### Gráficos de Línea
- Evolución temporal de montos
- Tendencias de transacciones
- Patrones estacionales

### Gráficos de Barras
- Distribución por categorías
- Comparaciones entre grupos
- Rankings de valores

### Gráficos de Torta
- Distribución porcentual
- Proporciones por categoría
- Segmentación de datos

### Gráficos 3D
- Clustering de transacciones
- Análisis multidimensional
- Patrones complejos

## 📤 Exportación de Datos

### Formatos Disponibles
- **CSV**: Para análisis en Excel/Google Sheets
- **JSON**: Para integración con APIs
- **Filtros Aplicados**: Solo datos seleccionados
- **Timestamp**: Incluye fecha y hora de exportación

### Opciones de Exportación
- Datos completos
- Datos filtrados
- Resumen estadístico
- Anomalías detectadas

## 🔍 Casos de Uso

### Para Analistas Financieros
- Monitoreo de transacciones en tiempo real
- Detección de patrones inusuales
- Análisis de riesgo
- Reportes automáticos

### Para Desarrolladores
- Integración con APIs
- Análisis de rendimiento
- Debugging de transacciones
- Monitoreo de sistemas

### Para Gestores
- Dashboards ejecutivos
- Métricas de negocio
- Alertas automáticas
- Reportes de cumplimiento

## 🛠️ Personalización

### Temas
- Colores personalizables
- Layouts adaptativos
- Iconos y branding
- Estilos CSS

### Métricas Personalizadas
- KPIs específicos
- Alertas personalizadas
- Umbrales configurables
- Notificaciones

### Integraciones
- APIs externas
- Servicios de notificación
- Sistemas de monitoreo
- Bases de datos adicionales

## 📱 Responsive Design

### Dispositivos Soportados
- **Desktop**: Pantallas grandes
- **Tablet**: Pantallas medianas
- **Mobile**: Dispositivos móviles
- **Adaptativo**: Ajuste automático

### Características Responsive
- Layouts flexibles
- Gráficos adaptativos
- Navegación táctil
- Contenido optimizado

## 🔒 Seguridad

### Acceso a Datos
- Conexión segura a PostgreSQL
- Autenticación de base de datos
- Encriptación de conexión
- Logs de acceso

### Privacidad
- No almacenamiento local de datos sensibles
- Conexión directa a base de datos
- Filtros de datos por usuario
- Auditoría de accesos

## 📈 Rendimiento

### Optimizaciones
- Consultas eficientes
- Índices de base de datos
- Caché de datos
- Lazy loading

### Escalabilidad
- Procesamiento por lotes
- Paginación de resultados
- Compresión de datos
- CDN para assets

## 🆘 Soporte y Troubleshooting

### Problemas Comunes
1. **Error de conexión a BD**: Verificar credenciales
2. **Dependencias faltantes**: Ejecutar `pip install -r requirements.txt`
3. **Puerto ocupado**: Cambiar puerto en configuración
4. **Datos no cargan**: Verificar consulta SQL

### Logs y Debugging
- Logs detallados en consola
- Archivos de log automáticos
- Métricas de rendimiento
- Alertas de error

## 🚀 Próximas Funcionalidades

### En Desarrollo
- Análisis de sentimientos
- Predicciones avanzadas
- Alertas en tiempo real
- Integración con más blockchains

### Roadmap
- Machine Learning avanzado
- Visualizaciones 3D
- APIs REST
- Aplicación móvil

---

**Dashboard desarrollado con ❤️ para análisis avanzado de blockchain Corda**
