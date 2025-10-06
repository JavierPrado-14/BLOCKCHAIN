# 🔗 Corda Blockchain ETL + Dashboard con IA

## 📋 Descripción del Proyecto

Sistema completo de **ETL (Extract, Transform, Load)** para datos de blockchain Corda, integrado con un **dashboard interactivo con capacidades de Inteligencia Artificial** usando Streamlit, Plotly y scikit-learn.

## ✨ Características Principales

### 🔄 Proceso ETL
- **Extracción**: Datos de blockchain Corda (simulados)
- **Transformación**: Limpieza y estructuración de datos
- **Carga**: Base de datos PostgreSQL en Render
- **Validación**: Verificación de integridad de datos

### 📊 Dashboard con IA
- **Visualizaciones Interactivas**: Streamlit + Plotly
- **Machine Learning**: Detección de anomalías y clustering
- **Análisis Temporal**: Series de tiempo y tendencias
- **Filtros Dinámicos**: Por fecha, moneda, tipo de estado
- **Exportación**: Datos en CSV y JSON

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.8+
- PostgreSQL (base de datos en Render)
- Dependencias instaladas

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/CarlosAHP/blockchainjp.git
cd blockchainjp

# Instalar dependencias
pip install -r requirements.txt

# Verificar configuración
python test_dashboard.py
```

### Ejecución
```bash
# Ejecutar ETL
python corda_etl_postgresql.py

# Ejecutar dashboard
streamlit run corda_dashboard.py

# O usar script de inicio
python start_dashboard.py
```

## 📁 Estructura del Proyecto

```
├── corda_etl_postgresql.py      # ETL principal con PostgreSQL
├── corda_dashboard.py           # Dashboard con IA
├── start_dashboard.py           # Script de inicio rápido
├── test_dashboard.py           # Pruebas del sistema
├── verify_postgresql.py         # Verificación de BD
├── config.ini                   # Configuración del sistema
├── requirements.txt             # Dependencias Python
├── .streamlit/config.toml       # Configuración de Streamlit
├── README.md                    # Este archivo
├── DASHBOARD_README.md          # Documentación del dashboard
├── ETL_SUMMARY.md              # Documentación del ETL
└── PROJECT_SUMMARY.md          # Resumen completo del proyecto
```

## 📊 Datos Procesados

### Estadísticas
- **Total Transacciones**: 150+ registros
- **Monto Total**: $397,196,060.15
- **Monto Promedio**: $2,647,973.73
- **Monedas**: 7 (USD, EUR, GBP, JPY, CHF, CAD, AUD)
- **Tipos de Estado**: 7 (LoanState, AssetState, etc.)

### Base de Datos
- **PostgreSQL**: Conectado a Render
- **Tabla**: `corda_transactions`
- **Índices**: Optimizados para consultas rápidas
- **Estructura**: 16 campos con metadatos completos

## 🤖 Capacidades de IA

### Machine Learning
- **Detección de Anomalías**: Isolation Forest
- **Clustering**: K-Means con visualización 3D
- **Análisis Predictivo**: Tendencias y patrones
- **Clasificación**: Estados de transacciones

### Visualizaciones
- **Series Temporales**: Evolución de transacciones
- **Análisis por Moneda**: Distribución y montos
- **Análisis por Estado**: Tipos de transacciones
- **Análisis de Status**: Estados de confirmación

## 🔧 Configuración

### Base de Datos
```ini
[DATABASE]
db_host = dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com
db_port = 5432
db_name = blokchain_bd
db_user = blokchain_bd_user
db_password = RlxkDsSrWcte8ASrxsztagJWod7qNrWP
```

### Dashboard
- **URL**: http://localhost:8501
- **Puerto**: 8501 (configurable)
- **Tema**: Personalizable
- **Responsive**: Móvil y desktop

## 📈 Funcionalidades

### ETL
- ✅ Conexión a PostgreSQL en Render
- ✅ Extracción de datos simulados
- ✅ Transformación y limpieza
- ✅ Carga con validación
- ✅ Logging detallado

### Dashboard
- ✅ Métricas en tiempo real
- ✅ Filtros interactivos
- ✅ Visualizaciones dinámicas
- ✅ Análisis con IA
- ✅ Exportación de datos

## 🛠️ Tecnologías

### Backend
- **Python 3.13**: Lenguaje principal
- **PostgreSQL**: Base de datos
- **SQLAlchemy**: ORM
- **Psycopg2**: Driver de PostgreSQL

### Frontend
- **Streamlit**: Framework de dashboard
- **Plotly**: Visualizaciones interactivas
- **HTML/CSS**: Estilos personalizados

### Machine Learning
- **Scikit-learn**: Algoritmos de ML
- **Isolation Forest**: Detección de anomalías
- **K-Means**: Clustering
- **StandardScaler**: Normalización

## 📱 Responsive Design

- ✅ **Desktop**: Pantallas grandes
- ✅ **Tablet**: Pantallas medianas
- ✅ **Mobile**: Dispositivos móviles
- ✅ **Adaptativo**: Ajuste automático

## 🔒 Seguridad

- ✅ Conexión segura a PostgreSQL
- ✅ Autenticación de base de datos
- ✅ Encriptación de conexión
- ✅ Logs de acceso

## 📤 Exportación

### Formatos Disponibles
- **CSV**: Para análisis en Excel
- **JSON**: Para integración con APIs
- **Filtros Aplicados**: Solo datos seleccionados
- **Timestamp**: Incluye fecha y hora

## 🚀 Próximos Pasos

### Mejoras Inmediatas
- Conexión a API real de Corda
- Más algoritmos de ML
- Alertas en tiempo real
- Integración con más blockchains

### Roadmap
- Machine Learning avanzado
- Visualizaciones 3D
- APIs REST
- Aplicación móvil nativa

## 📞 Soporte

### Problemas Comunes
1. **Error de conexión a BD**: Verificar credenciales
2. **Dependencias faltantes**: `pip install -r requirements.txt`
3. **Puerto ocupado**: Cambiar puerto en configuración
4. **Datos no cargan**: Verificar consulta SQL

### Logs
- Logs detallados en consola
- Archivos de log automáticos
- Métricas de rendimiento
- Alertas de error

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios
4. Crear Pull Request

## 📧 Contacto

- **GitHub**: [CarlosAHP](https://github.com/CarlosAHP)
- **Repositorio**: [blockchainjp](https://github.com/CarlosAHP/blockchainjp)

---

**Desarrollado con ❤️ para análisis avanzado de blockchain Corda**

*Última actualización: 2025-10-05*