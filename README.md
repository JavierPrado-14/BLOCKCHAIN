# 🚀 Dashboard de Corda Blockchain con Gemini AI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-14+-blue.svg)](https://www.postgresql.org/)
[![Gemini AI](https://img.shields.io/badge/gemini-2.5--flash-green.svg)](https://ai.google.dev/)

## 📋 Descripción

**Dashboard interactivo de análisis en tiempo real** para transacciones de blockchain Corda, potenciado por **Gemini AI** de Google para generar insights inteligentes y análisis contextual.

### ✨ Características Principales

- 🔄 **Datos en Tiempo Real**: Consultas dinámicas a PostgreSQL
- 🧠 **Análisis con IA**: Gemini 2.5 Flash para insights contextuales
- 📊 **Visualizaciones Avanzadas**: Gráficos interactivos con Plotly
- 🤖 **Machine Learning**: Detección de anomalías y clustering
- ⏰ **Auto-actualización**: Configurable de 10s a 5min
- 🎯 **Filtros Granulares**: Por fecha, moneda, estado, monto
- 📈 **100,000+ Transacciones**: Dataset sintético realista

---

## 🚀 Inicio Rápido

### 1️⃣ Instalación

```bash
# Clonar el repositorio
git clone https://github.com/JavierPrado-14/BLOCKCHAIN.git
cd BLOCKCHAIN/blockchainjp

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\Activate.ps1

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Ejecutar Dashboard

```bash
# Método 1: Directo
streamlit run corda_dashboard.py

# Método 2: Con script mejorado
python start_dashboard_gemini.py
```

### 3️⃣ Acceder al Dashboard

🌐 Abrir en navegador: **http://localhost:8501**

---

## 📊 Funcionalidades Principales

### 🔄 Dashboard en Tiempo Real

- **Consultas Dinámicas**: Los datos se cargan desde PostgreSQL en tiempo real
- **Filtros Temporales**: Última hora, 24h, 7d, 30d, todo el tiempo
- **Auto-actualización**: Configurable para refrescar datos automáticamente
- **Estadísticas en Vivo**: Métricas actualizadas constantemente

### 🧠 Análisis con Gemini AI

- **Modelo**: Gemini 2.5 Flash (última versión de Google)
- **Análisis Contextual**: Adaptado al período temporal seleccionado
- **Insights Específicos**: Patrones, tendencias, anomalías
- **Recomendaciones**: Accionables para toma de decisiones
- **Predicciones**: Basadas en datos históricos

### 📈 Visualizaciones Avanzadas

1. **Series Temporales**: Evolución de transacciones en el tiempo
2. **Análisis por Moneda**: Distribución y montos por divisa
3. **Análisis por Estado**: Estados de transacciones
4. **Machine Learning**: Detección de anomalías y clustering

### 🎯 Controles Interactivos

- **Filtros de Fecha**: Rango personalizable
- **Filtros de Moneda**: USD, EUR, GBP, JPY, etc.
- **Filtros de Estado**: CONFIRMED, PENDING, FAILED, CANCELLED
- **Filtros de Monto**: Rango mínimo y máximo
- **Exportación**: CSV y JSON

---

## 📁 Estructura del Proyecto

```
blockchainjp/
├── corda_dashboard.py              # ⭐ Dashboard principal con Gemini AI
├── requirements.txt                # 📦 Dependencias del proyecto
├── config.ini                      # ⚙️ Configuración de base de datos
├── start_dashboard_gemini.py       # 🚀 Script de inicio mejorado
├── generador_incremental.py        # 🔄 Generador de datos sintéticos
├── README.md                       # 📖 Este archivo
├── PROYECTO_COMPLETO_RESUMEN.md    # 📋 Resumen completo del proyecto
├── DASHBOARD_GEMINI_README.md      # 📚 Guía detallada Gemini AI
└── .gitignore                      # 🚫 Archivos a ignorar en Git
```

---

## 🗄️ Base de Datos

### Configuración PostgreSQL

```ini
[DATABASE]
host = dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com
port = 5432
database = blokchain_bd
user = blokchain_bd_user
password = RlxkDsSrWcte8ASrxsztagJWod7qNrWP
```

### Datos Disponibles

- **Total de Transacciones**: 100,000
- **Período**: 2022-10-11 a 2025-10-10 (3 años)
- **Monedas**: USD, EUR, GBP, JPY, AUD, CAD, CHF, CNY, BRL, MXN
- **Estados**: CONFIRMED, PENDING, FAILED, CANCELLED
- **Redes**: CordaNetwork, TestNetwork, MainNetwork

### Origen de los Datos

Los datos son **sintéticos** (generados por `generador_incremental.py`) con:
- ✅ Estructura real de Corda
- ✅ Patrones realistas de actividad
- ✅ Distribución de montos ponderada
- ✅ Horarios de actividad simulados

---

## 🤖 Configuración de Gemini AI

### API Key

El dashboard usa Gemini AI con la siguiente configuración:

```python
GEMINI_API_KEY = "AIzaSyBM5jwwPLcn9aldmaypSP-ywvqecVfJEIA"
model = genai.GenerativeModel('gemini-2.5-flash')
```

### Uso de Gemini

1. **Scroll** hasta la sección "🧠 Insights Generados por IA"
2. **Clic** en "✨ Generar Análisis IA"
3. **Esperar** 3-5 segundos mientras Gemini analiza
4. **Leer** insights específicos del período seleccionado

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.8+**: Lenguaje principal
- **PostgreSQL**: Base de datos (Render.com)
- **Psycopg2**: Driver de PostgreSQL

### Frontend
- **Streamlit 1.28**: Framework de dashboard
- **Plotly 5.17**: Visualizaciones interactivas
- **Pandas**: Manipulación de datos

### IA y Machine Learning
- **Google Gemini 2.5 Flash**: Análisis inteligente
- **Scikit-learn 1.3**: ML para anomalías y clustering
- **Isolation Forest**: Detección de anomalías
- **K-Means**: Clustering

---

## 📖 Guías de Uso

### 1. Configurar Análisis en Tiempo Real

1. **Sidebar** → "⏰ Controles de Tiempo Real"
2. **Modo de Análisis** → Seleccionar período (ej: "Últimas 24h")
3. **Auto-actualización** → ✅ Activar
4. **Intervalo** → Configurar (ej: 60 segundos)

### 2. Generar Análisis IA

1. **Scroll** hasta "🧠 Insights Generados por IA"
2. **Clic** en "✨ Generar Análisis IA"
3. **Leer** insights específicos del período

### 3. Aplicar Filtros

1. **Sidebar** → "🔧 Filtros Interactivos"
2. **Filtrar** por fecha, moneda, estado, monto
3. **Ver** datos filtrados en tiempo real

### 4. Exportar Datos

1. **Sidebar** → "📤 Exportar Datos"
2. **Seleccionar** formato (CSV o JSON)
3. **Descargar** archivo con datos filtrados

---

## 🔧 Generar Más Datos

Si necesitas generar más datos sintéticos:

```bash
# Ejecutar generador incremental
python generador_incremental.py

# El script:
# - Verifica datos existentes
# - Genera solo los faltantes
# - Maneja desconexiones automáticamente
# - Inserta en lotes de 2,000
```

---

## 💡 Características Destacadas

### ✅ Datos Dinámicos

- **Antes**: 150 transacciones fijas en el código
- **Ahora**: 100,000+ transacciones en PostgreSQL con consultas dinámicas

### ✅ Análisis Contextual

- **Antes**: Análisis genérico sin contexto
- **Ahora**: Gemini AI analiza el período temporal específico

### ✅ Tiempo Real

- **Antes**: Datos estáticos sin actualización
- **Ahora**: Auto-actualización configurable y estadísticas en vivo

### ✅ Insights Inteligentes

- **Antes**: Sin IA
- **Ahora**: Gemini AI genera insights, patrones, y recomendaciones

---

## 🐛 Solución de Problemas

### Error de Conexión a PostgreSQL

```bash
# Verificar conexión
python -c "import psycopg2; conn = psycopg2.connect(host='dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com', port=5432, database='blokchain_bd', user='blokchain_bd_user', password='RlxkDsSrWcte8ASrxsztagJWod7qNrWP'); print('✅ Conectado')"
```

### Puerto 8501 Ocupado

```bash
# Cambiar puerto
streamlit run corda_dashboard.py --server.port 8502
```

### Dependencias Faltantes

```bash
# Reinstalar todas las dependencias
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Documentación Adicional

- **`PROYECTO_COMPLETO_RESUMEN.md`**: Resumen técnico completo del proyecto
- **`DASHBOARD_GEMINI_README.md`**: Guía detallada de Gemini AI integration
- **`config.ini`**: Configuración de base de datos

---

## 🎯 Próximos Pasos Sugeridos

### Mejoras Inmediatas
1. **Conectar a Corda Real**: Crear ETL para nodo Corda en producción
2. **Alertas Automáticas**: Notificaciones por email de anomalías
3. **Dashboard Móvil**: Versión responsive optimizada

### Mejoras Futuras
1. **Análisis Comparativo**: Comparar períodos diferentes
2. **Más Modelos de IA**: GPT-4, Claude, etc.
3. **API REST**: Exponer datos via API
4. **Multi-blockchain**: Soporte para Ethereum, Bitcoin, etc.

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

1. Fork del repositorio
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

---

## 📧 Contacto

- **GitHub**: [JavierPrado-14](https://github.com/JavierPrado-14)
- **Repositorio**: [BLOCKCHAIN](https://github.com/JavierPrado-14/BLOCKCHAIN.git)

---

## 🎉 Resultado Final

**¡PROYECTO COMPLETADO EXITOSAMENTE!**

- 🔄 **Datos dinámicos** desde PostgreSQL en tiempo real
- 🧠 **Análisis inteligente** con Gemini AI
- 📊 **100,000+ transacciones** de datos sintéticos realistas
- 📈 **Visualizaciones avanzadas** e interactivas
- 🎯 **Controles granulares** de tiempo y filtros
- 💡 **Insights accionables** para toma de decisiones

**🌐 Visita tu dashboard en: http://localhost:8501**

---

**Desarrollado con ❤️ para análisis avanzado de blockchain Corda**

*Última actualización: Octubre 2025*