# 🤖 Dashboard Corda con Gemini AI - Guía de Uso

## 📋 Resumen

El dashboard ahora incluye **dos nuevas funcionalidades principales**:

1. **🔄 Botón de Actualización de Datos** - Refresca los datos desde la base de datos en tiempo real
2. **🧠 Análisis con IA Generativa (Gemini)** - Genera insights inteligentes automáticamente

---

## ✨ Nuevas Funcionalidades

### 1. 🔄 Actualización de Datos

**Ubicación:** Esquina superior derecha del dashboard

**Funcionalidad:**
- Botón azul "🔄 Actualizar Datos"
- Recarga todos los datos desde PostgreSQL
- Actualiza todas las visualizaciones y métricas
- Muestra timestamp de última actualización

**Uso:**
```
1. Haz clic en "🔄 Actualizar Datos"
2. Espera mientras se cargan los datos (spinner aparece)
3. El dashboard se refresca automáticamente con los nuevos datos
```

---

### 2. 🧠 Insights Generados por IA (Gemini)

**Ubicación:** Primera sección después de las métricas principales

**Funcionalidad:**
- Botón "✨ Generar Análisis IA"
- Análisis automático de patrones y tendencias
- Detección de anomalías
- Recomendaciones basadas en datos
- Predicciones sobre comportamiento futuro

**Uso:**
```
1. Haz clic en "✨ Generar Análisis IA"
2. Espera mientras Gemini analiza los datos (spinner aparece)
3. Lee el análisis inteligente generado
4. Los insights se guardan en la sesión hasta que actualices
```

**Qué Analiza Gemini:**
- ✅ Estadísticas generales (total, promedio, rangos)
- ✅ Distribución por moneda
- ✅ Distribución por estado de transacciones
- ✅ Patrones temporales (horas, días más activos)
- ✅ Tendencias y anomalías
- ✅ Recomendaciones prácticas

---

## 🚀 Cómo Ejecutar el Dashboard

### Opción 1: Usando el script de inicio
```bash
cd blockchainjp
.\venv\Scripts\Activate.ps1
streamlit run corda_dashboard.py
```

### Opción 2: Usando el archivo de inicio directo
```bash
cd blockchainjp
python start_dashboard.py
```

---

## 🔧 Configuración de Gemini AI

### API Key
La API key de Gemini ya está configurada en el código:
```python
GEMINI_API_KEY = "AIzaSyBM5jwwPLcn9aldmaypSP-ywvqecVfJEIA"
```

### Modelo
Se utiliza el modelo **Gemini 2.5 Flash** (última versión estable) para análisis rápidos:
```python
self.model = genai.GenerativeModel('gemini-2.5-flash')
```

---

## 📊 Flujo de Trabajo Recomendado

1. **Iniciar el Dashboard**
   ```bash
   streamlit run corda_dashboard.py
   ```

2. **Actualizar Datos**
   - Clic en "🔄 Actualizar Datos" para obtener los datos más recientes

3. **Generar Insights de IA**
   - Clic en "✨ Generar Análisis IA" para obtener análisis inteligente

4. **Explorar Visualizaciones**
   - Series temporales
   - Análisis por moneda
   - Análisis por estado
   - Machine Learning (anomalías y clusters)

5. **Aplicar Filtros** (Sidebar)
   - Rango de fechas
   - Monedas específicas
   - Tipos de estado
   - Rangos de monto

6. **Exportar Datos**
   - Descargar CSV
   - Descargar JSON

---

## 🎯 Características del Análisis IA

### Análisis Automático
- **Patrones Principales:** Identifica tendencias clave
- **Distribuciones:** Analiza monedas, estados y tipos
- **Temporalidad:** Detecta horarios y días más activos
- **Anomalías:** Señala comportamientos inusuales
- **Recomendaciones:** Sugiere acciones basadas en datos

### Ventajas
- ✅ Análisis en lenguaje natural (español)
- ✅ Insights contextualizados
- ✅ Detección automática de patrones
- ✅ Recomendaciones accionables
- ✅ Actualizable en tiempo real

---

## 🔒 Seguridad

⚠️ **IMPORTANTE:** 
- La API key está hardcodeada para fines de desarrollo
- Para producción, considera usar variables de entorno:
  ```python
  import os
  GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
  ```

---

## 📦 Dependencias Nuevas

Se agregó al `requirements.txt`:
```
google-generativeai==0.3.2
```

Para instalar:
```bash
pip install google-generativeai
```

---

## 🐛 Solución de Problemas

### Error: "No se puede importar google.generativeai"
```bash
# Activa el entorno virtual
.\venv\Scripts\Activate.ps1

# Instala la dependencia
pip install google-generativeai
```

### Error: "API Key inválida"
- Verifica que la API key esté correcta
- Asegúrate de tener acceso a internet
- Revisa la cuota de la API en Google Cloud Console

### El botón de actualización no funciona
- Verifica la conexión a PostgreSQL
- Revisa los logs en la consola
- Asegúrate de que las credenciales de BD sean correctas

---

## 📈 Mejoras Futuras

- [ ] Caché de análisis de IA
- [ ] Múltiples modelos de IA (GPT, Claude, etc.)
- [ ] Análisis comparativo entre períodos
- [ ] Alertas automáticas basadas en IA
- [ ] Exportar insights en PDF

---

## 📞 Contacto y Soporte

Para preguntas o problemas:
1. Revisa esta documentación
2. Consulta los logs del dashboard
3. Verifica la conexión a PostgreSQL y Gemini API

---

## 📝 Changelog

### Versión 2.0 (Actual)
- ✅ Agregado botón de actualización de datos
- ✅ Integración con Gemini AI
- ✅ Análisis inteligente automático
- ✅ Timestamp de última actualización
- ✅ Session state para guardar insights

### Versión 1.0
- Dashboard básico con visualizaciones
- Análisis de Machine Learning
- Filtros interactivos
- Exportación de datos

---

**¡Disfruta del nuevo dashboard mejorado con IA! 🚀**

