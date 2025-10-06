#!/usr/bin/env python3
"""
Script para verificar los datos cargados en PostgreSQL en Render
"""

import psycopg2
import pandas as pd
import json
from datetime import datetime

def verify_postgresql_data():
    """Verificar los datos en PostgreSQL"""
    print("Verificando datos en PostgreSQL en Render...")
    print("=" * 60)
    
    # Configuración de conexión
    db_config = {
        'host': 'dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com',
        'port': 5432,
        'database': 'blokchain_bd',
        'user': 'blokchain_bd_user',
        'password': 'RlxkDsSrWcte8ASrxsztagJWod7qNrWP'
    }
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        print("OK: Conexion exitosa a PostgreSQL en Render")
        
        # Verificar tabla
        cursor.execute("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'corda_transactions'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        print(f"\nEstructura de la tabla 'corda_transactions':")
        for col in columns:
            print(f"  {col[1]}: {col[2]}")
        
        # Estadísticas básicas
        cursor.execute("SELECT COUNT(*) FROM corda_transactions")
        total_count = cursor.fetchone()[0]
        print(f"\nTotal de registros: {total_count}")
        
        # Mostrar algunos registros de ejemplo
        cursor.execute("""
            SELECT id, timestamp, state_type, amount, currency, status 
            FROM corda_transactions 
            ORDER BY timestamp DESC 
            LIMIT 5
        """)
        sample_data = cursor.fetchall()
        
        print(f"\nUltimos 5 registros:")
        for row in sample_data:
            print(f"  ID: {row[0]}")
            print(f"  Timestamp: {row[1]}")
            print(f"  Estado: {row[2]}")
            print(f"  Monto: ${row[3]:,.2f} {row[4]}")
            print(f"  Status: {row[5]}")
            print("  ---")
        
        # Estadísticas detalladas
        stats_query = """
        SELECT 
            COUNT(*) as total_transactions,
            COUNT(DISTINCT state_type) as unique_state_types,
            COUNT(DISTINCT currency) as unique_currencies,
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount,
            MIN(timestamp) as earliest_transaction,
            MAX(timestamp) as latest_transaction
        FROM corda_transactions
        """
        
        cursor.execute(stats_query)
        stats = cursor.fetchone()
        
        print(f"\nEstadisticas de la base de datos:")
        print(f"  Total transacciones: {stats[0]}")
        print(f"  Tipos de estado únicos: {stats[1]}")
        print(f"  Monedas únicas: {stats[2]}")
        print(f"  Monto total: ${stats[3]:,.2f}")
        print(f"  Monto promedio: ${stats[4]:,.2f}")
        print(f"  Transacción más antigua: {stats[5]}")
        print(f"  Transacción más reciente: {stats[6]}")
        
        # Distribución por tipo de estado
        cursor.execute("""
            SELECT state_type, COUNT(*) as count 
            FROM corda_transactions 
            GROUP BY state_type 
            ORDER BY count DESC
        """)
        state_dist = cursor.fetchall()
        
        print(f"\nDistribucion por tipo de estado:")
        for state_type, count in state_dist:
            print(f"  {state_type}: {count}")
        
        # Distribución por moneda
        cursor.execute("""
            SELECT currency, COUNT(*) as count 
            FROM corda_transactions 
            GROUP BY currency 
            ORDER BY count DESC
        """)
        currency_dist = cursor.fetchall()
        
        print(f"\nDistribucion por moneda:")
        for currency, count in currency_dist:
            print(f"  {currency}: {count}")
        
        # Distribución por status
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM corda_transactions 
            GROUP BY status 
            ORDER BY count DESC
        """)
        status_dist = cursor.fetchall()
        
        print(f"\nDistribucion por status:")
        for status, count in status_dist:
            print(f"  {status}: {count}")
        
        cursor.close()
        conn.close()
        
        print("\nOK: Verificacion completada exitosamente")
        print("Los datos estan listos para el dashboard con IA!")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Error verificando datos: {str(e)}")
        return False

if __name__ == "__main__":
    verify_postgresql_data()
