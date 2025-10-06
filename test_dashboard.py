#!/usr/bin/env python3
"""
Script de prueba para el dashboard de Corda
Verifica la conectividad y funcionalidades del dashboard
"""

import psycopg2
import pandas as pd
from datetime import datetime

def test_database_connection():
    """Probar conexión a la base de datos"""
    print("Probando conexion a PostgreSQL...")
    
    db_config = {
        'host': 'dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com',
        'port': 5432,
        'database': 'blokchain_bd',
        'user': 'blokchain_bd_user',
        'password': 'RlxkDsSrWcte8ASrxsztagJWod7qNrWP'
    }
    
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Verificar tabla
        cursor.execute("SELECT COUNT(*) FROM corda_transactions")
        count = cursor.fetchone()[0]
        
        # Obtener estadísticas básicas
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(amount) as total_amount,
                AVG(amount) as avg_amount,
                COUNT(DISTINCT currency) as currencies,
                COUNT(DISTINCT state_type) as state_types
            FROM corda_transactions
        """)
        stats = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print("OK: Conexion exitosa a PostgreSQL")
        print(f"  - Total transacciones: {count}")
        print(f"  - Monto total: ${stats[1]:,.2f}")
        print(f"  - Monto promedio: ${stats[2]:,.2f}")
        print(f"  - Monedas: {stats[3]}")
        print(f"  - Tipos de estado: {stats[4]}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Error conectando a PostgreSQL: {str(e)}")
        return False

def test_dashboard_requirements():
    """Probar dependencias del dashboard"""
    print("\nProbando dependencias del dashboard...")
    
    try:
        import streamlit as st
        print("OK: Streamlit instalado")
        
        import plotly.express as px
        import plotly.graph_objects as go
        print("OK: Plotly instalado")
        
        import pandas as pd
        print("OK: Pandas disponible")
        
        import numpy as np
        print("OK: NumPy disponible")
        
        from sklearn.ensemble import IsolationForest
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans
        print("OK: Scikit-learn disponible")
        
        return True
        
    except ImportError as e:
        print(f"ERROR: Dependencia faltante: {str(e)}")
        return False

def test_data_processing():
    """Probar procesamiento de datos"""
    print("\nProbando procesamiento de datos...")
    
    try:
        # Simular carga de datos
        db_config = {
            'host': 'dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com',
            'port': 5432,
            'database': 'blokchain_bd',
            'user': 'blokchain_bd_user',
            'password': 'RlxkDsSrWcte8ASrxsztagJWod7qNrWP'
        }
        
        conn = psycopg2.connect(**db_config)
        query = "SELECT * FROM corda_transactions LIMIT 10"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if len(df) > 0:
            print(f"OK: Datos cargados correctamente ({len(df)} registros)")
            
            # Probar procesamiento básico
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['amount_numeric'] = pd.to_numeric(df['amount'], errors='coerce')
            
            print("OK: Procesamiento de datos exitoso")
            return True
        else:
            print("ERROR: No hay datos en la base de datos")
            return False
            
    except Exception as e:
        print(f"ERROR: Error procesando datos: {str(e)}")
        return False

def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("PRUEBA DEL DASHBOARD CORDA BLOCKCHAIN")
    print("=" * 60)
    
    # Probar conexión a base de datos
    db_ok = test_database_connection()
    
    # Probar dependencias
    deps_ok = test_dashboard_requirements()
    
    # Probar procesamiento de datos
    data_ok = test_data_processing()
    
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    if db_ok and deps_ok and data_ok:
        print("OK: TODAS LAS PRUEBAS EXITOSAS")
        print("El dashboard esta listo para usar!")
        print("\nPara ejecutar el dashboard:")
        print("  streamlit run corda_dashboard.py")
        print("\nEl dashboard estara disponible en:")
        print("  http://localhost:8501")
    else:
        print("ERROR: ALGUNAS PRUEBAS FALLARON")
        if not db_ok:
            print("  - Problema con la conexion a PostgreSQL")
        if not deps_ok:
            print("  - Problema con las dependencias")
        if not data_ok:
            print("  - Problema con el procesamiento de datos")

if __name__ == "__main__":
    main()
