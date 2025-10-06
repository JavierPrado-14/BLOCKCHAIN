# 🚀 Guía de Configuración - Corda Blockchain ETL + Dashboard

## 📋 Pasos para Configurar el Proyecto

### 1. 🔧 Configuración Inicial

```bash
# Clonar el repositorio
git clone https://github.com/CarlosAHP/blockchainjp.git
cd blockchainjp

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. 🗄️ Configuración de Base de Datos

El proyecto está configurado para usar PostgreSQL en Render. Las credenciales están en `config.ini`:

```ini
[DATABASE]
db_host = dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com
db_port = 5432
db_name = blokchain_bd
db_user = blokchain_bd_user
db_password = RlxkDsSrWcte8ASrxsztagJWod7qNrWP
```

### 3. 🧪 Verificar Configuración

```bash
# Probar conexión a base de datos
python verify_postgresql.py

# Probar dependencias del dashboard
python test_dashboard.py
```

### 4. 🔄 Ejecutar ETL

```bash
# Generar datos y cargar a PostgreSQL
python corda_etl_postgresql.py
```

### 5. 📊 Ejecutar Dashboard

```bash
# Opción 1: Script de inicio automático
python start_dashboard.py

# Opción 2: Ejecutar directamente
streamlit run corda_dashboard.py
```

### 6. 🌐 Acceder al Dashboard

- **URL Local**: http://localhost:8501
- **URL de Red**: http://[tu-ip]:8501
- **Dispositivos Móviles**: Misma red local

## 🔧 Configuración Avanzada

### Cambiar Puerto del Dashboard

Editar `.streamlit/config.toml`:
```toml
[server]
port = 8502  # Cambiar puerto
```

### Configurar Base de Datos Local

Editar `config.ini`:
```ini
[DATABASE]
db_type = postgresql
db_host = localhost
db_port = 5432
db_name = tu_base_datos
db_user = tu_usuario
db_password = tu_contraseña
```

### Personalizar Dashboard

Editar `corda_dashboard.py`:
- Cambiar colores en CSS
- Agregar nuevas visualizaciones
- Modificar filtros
- Personalizar métricas

## 📊 Datos de Ejemplo

El proyecto incluye datos simulados de blockchain Corda:

- **150+ transacciones** con datos realistas
- **$397M+** en montos procesados
- **7 monedas** diferentes
- **7 tipos de estado** de transacciones
- **30 días** de datos temporales

## 🤖 Funcionalidades de IA

### Detección de Anomalías
- Algoritmo: Isolation Forest
- Identifica transacciones inusuales
- Visualización automática

### Clustering
- Algoritmo: K-Means
- Agrupa transacciones similares
- Gráfico 3D interactivo

### Análisis Predictivo
- Tendencias temporales
- Patrones de comportamiento
- Correlaciones entre variables

## 📱 Uso del Dashboard

### Navegación
1. **Métricas Principales**: Resumen en la parte superior
2. **Filtros**: Barra lateral izquierda
3. **Visualizaciones**: Gráficos interactivos
4. **Análisis IA**: Sección de Machine Learning
5. **Exportación**: Botones de descarga

### Filtros Disponibles
- **Rango de Fechas**: Selector de fechas
- **Monedas**: Multi-selector
- **Tipos de Estado**: Multi-selector
- **Estados de Transacción**: Multi-selector
- **Rango de Monto**: Slider numérico

### Exportación
- **CSV**: Para análisis en Excel
- **JSON**: Para integración con APIs
- **Datos Filtrados**: Solo selección actual

## 🛠️ Solución de Problemas

### Error de Conexión a BD
```bash
# Verificar credenciales en config.ini
# Probar conexión manual
python verify_postgresql.py
```

### Dependencias Faltantes
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Puerto Ocupado
```bash
# Cambiar puerto en .streamlit/config.toml
# O usar puerto específico
streamlit run corda_dashboard.py --server.port 8502
```

### Datos No Cargan
```bash
# Verificar consulta SQL
# Revisar logs en consola
# Probar con datos de ejemplo
python demo_etl.py
```

## 📈 Rendimiento

### Optimizaciones
- Índices en base de datos
- Consultas eficientes
- Caché de datos
- Lazy loading

### Escalabilidad
- Procesamiento por lotes
- Paginación de resultados
- Compresión de datos
- CDN para assets

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

## 📞 Soporte

### Logs y Debugging
- Logs detallados en consola
- Archivos de log automáticos
- Métricas de rendimiento
- Alertas de error

### Documentación
- `README.md`: Información general
- `DASHBOARD_README.md`: Documentación del dashboard
- `ETL_SUMMARY.md`: Documentación del ETL
- `PROJECT_SUMMARY.md`: Resumen completo

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

---

**¡Proyecto listo para usar! 🎉**

*Para más información, consulta la documentación en el repositorio.*
