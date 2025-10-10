#!/usr/bin/env python3
"""
Script mejorado para iniciar el Dashboard de Corda con Gemini AI
Incluye verificaciones de dependencias y configuración
"""

import sys
import subprocess
import os

def check_dependencies():
    """Verificar que todas las dependencias estén instaladas"""
    print("=" * 70)
    print("🔍 VERIFICANDO DEPENDENCIAS")
    print("=" * 70)
    print()
    
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'psycopg2',
        'sklearn',
        'google.generativeai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            elif package == 'google.generativeai':
                __import__('google.generativeai')
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NO INSTALADO")
            missing_packages.append(package)
    
    print()
    
    if missing_packages:
        print("⚠️  Faltan dependencias. Instalando...")
        print()
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print()
    else:
        print("✨ Todas las dependencias están instaladas")
    
    print()

def check_database_connection():
    """Verificar conexión a la base de datos"""
    print("=" * 70)
    print("🗄️  VERIFICANDO CONEXIÓN A BASE DE DATOS")
    print("=" * 70)
    print()
    
    try:
        import psycopg2
        
        db_config = {
            'host': 'dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com',
            'port': 5432,
            'database': 'blokchain_bd',
            'user': 'blokchain_bd_user',
            'password': 'RlxkDsSrWcte8ASrxsztagJWod7qNrWP'
        }
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM corda_transactions")
        count = cursor.fetchone()[0]
        conn.close()
        
        print(f"   ✅ Conexión exitosa")
        print(f"   📊 {count} transacciones disponibles")
        print()
        return True
        
    except Exception as e:
        print(f"   ❌ Error de conexión: {str(e)}")
        print()
        return False

def check_gemini_api():
    """Verificar configuración de Gemini AI"""
    print("=" * 70)
    print("🤖 VERIFICANDO GEMINI AI")
    print("=" * 70)
    print()
    
    try:
        import google.generativeai as genai
        
        GEMINI_API_KEY = "AIzaSyBM5jwwPLcn9aldmaypSP-ywvqecVfJEIA"
        genai.configure(api_key=GEMINI_API_KEY)
        
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        print(f"   ✅ API configurada correctamente")
        print(f"   🧠 Modelo: gemini-2.5-flash")
        print()
        return True
        
    except Exception as e:
        print(f"   ⚠️  Advertencia: {str(e)}")
        print(f"   ℹ️  El dashboard funcionará pero sin análisis de IA")
        print()
        return False

def show_dashboard_info():
    """Mostrar información sobre las funcionalidades del dashboard"""
    print()
    print("=" * 70)
    print("✨ NUEVAS FUNCIONALIDADES DEL DASHBOARD")
    print("=" * 70)
    print()
    print("🔄 ACTUALIZACIÓN DE DATOS:")
    print("   • Botón en la esquina superior derecha")
    print("   • Refresca datos desde PostgreSQL en tiempo real")
    print("   • Muestra timestamp de última actualización")
    print()
    print("🧠 ANÁLISIS CON IA GENERATIVA (GEMINI):")
    print("   • Botón 'Generar Análisis IA'")
    print("   • Análisis automático de patrones y tendencias")
    print("   • Detección de anomalías inteligente")
    print("   • Recomendaciones basadas en datos")
    print("   • Predicciones sobre comportamiento futuro")
    print()
    print("📊 ANÁLISIS TRADICIONALES:")
    print("   • Series temporales")
    print("   • Distribución por moneda y estado")
    print("   • Machine Learning (anomalías y clustering)")
    print("   • Filtros interactivos avanzados")
    print()
    print("=" * 70)
    print()

def start_dashboard():
    """Iniciar el dashboard"""
    print("🚀 INICIANDO DASHBOARD DE CORDA CON GEMINI AI")
    print("=" * 70)
    print()
    print("📍 El dashboard se abrirá en tu navegador predeterminado")
    print("🌐 URL: http://localhost:8501")
    print()
    print("⚠️  Para detener el servidor, presiona Ctrl+C")
    print("=" * 70)
    print()
    
    # Iniciar Streamlit
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'corda_dashboard.py'])

def main():
    """Función principal"""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🔗 DASHBOARD CORDA BLOCKCHAIN CON GEMINI AI  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Verificaciones
    check_dependencies()
    db_connected = check_database_connection()
    gemini_connected = check_gemini_api()
    
    if not db_connected:
        print("⚠️  ADVERTENCIA: No se pudo conectar a la base de datos")
        print("   El dashboard se iniciará pero puede no mostrar datos")
        print()
    
    # Mostrar información
    show_dashboard_info()
    
    # Preguntar si desea continuar
    print("¿Deseas iniciar el dashboard? (S/n): ", end='')
    response = input().strip().lower()
    
    if response in ['', 's', 'si', 'y', 'yes']:
        print()
        start_dashboard()
    else:
        print()
        print("✋ Inicio cancelado")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("👋 Dashboard cerrado correctamente")
        print()
        sys.exit(0)

