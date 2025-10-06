#!/usr/bin/env python3
"""
Script de inicio rápido para el Dashboard de Corda
Verifica dependencias y ejecuta el dashboard
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Verificar que las dependencias estén instaladas"""
    print("Verificando dependencias...")
    
    required_packages = [
        'streamlit',
        'plotly', 
        'pandas',
        'numpy',
        'psycopg2',
        'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} - FALTANTE")
    
    if missing_packages:
        print(f"\nInstalando paquetes faltantes: {', '.join(missing_packages)}")
        for package in missing_packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print("✓ Dependencias instaladas")
    
    return len(missing_packages) == 0

def check_database_connection():
    """Verificar conexión a la base de datos"""
    print("\nVerificando conexión a PostgreSQL...")
    
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
        cursor.close()
        conn.close()
        
        print(f"✓ Conexión exitosa - {count} transacciones disponibles")
        return True
        
    except Exception as e:
        print(f"✗ Error de conexión: {str(e)}")
        return False

def start_dashboard():
    """Iniciar el dashboard"""
    print("\nIniciando Dashboard de Corda...")
    print("=" * 50)
    print("Dashboard disponible en: http://localhost:8501")
    print("Presiona Ctrl+C para detener")
    print("=" * 50)
    
    try:
        # Ejecutar streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'corda_dashboard.py',
            '--server.port', '8501',
            '--server.headless', 'true'
        ])
    except KeyboardInterrupt:
        print("\nDashboard detenido por el usuario")
    except Exception as e:
        print(f"Error ejecutando dashboard: {str(e)}")

def main():
    """Función principal"""
    print("🔗 CORDDA BLOCKCHAIN DASHBOARD")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        print("Error: No se pudieron instalar todas las dependencias")
        return False
    
    # Verificar conexión a base de datos
    if not check_database_connection():
        print("Error: No se pudo conectar a la base de datos")
        return False
    
    # Verificar que el archivo del dashboard existe
    if not Path('corda_dashboard.py').exists():
        print("Error: No se encontró el archivo corda_dashboard.py")
        return False
    
    print("\n✓ Todas las verificaciones exitosas")
    print("✓ Iniciando dashboard...")
    
    # Iniciar dashboard
    start_dashboard()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDashboard detenido. ¡Hasta luego!")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        sys.exit(1)
