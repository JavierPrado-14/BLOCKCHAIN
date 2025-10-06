#!/usr/bin/env python3
"""
Script para verificar la base de datos SQLite generada
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime

def verify_database():
    """Verificar el contenido de la base de datos"""
    print("Verificando base de datos SQLite...")
    print("=" * 50)
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('demo_blockchain_data.db')
        
        # Obtener información de la tabla
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Tablas en la base de datos: {[table[0] for table in tables]}")
        
        # Consultar datos de la tabla principal
        df = pd.read_sql_query("SELECT * FROM corda_transactions LIMIT 5", conn)
        
        print(f"\nTotal de registros: {len(pd.read_sql_query('SELECT * FROM corda_transactions', conn))}")
        print(f"\nPrimeros 5 registros:")
        print(df.to_string(index=False))
        
        # Estadísticas básicas
        stats_query = """
        SELECT 
            COUNT(*) as total_transactions,
            COUNT(DISTINCT state_type) as unique_state_types,
            COUNT(DISTINCT currency) as unique_currencies,
            SUM(amount) as total_amount,
            AVG(amount) as avg_amount
        FROM corda_transactions
        """
        
        stats = pd.read_sql_query(stats_query, conn)
        print(f"\nEstadisticas de la base de datos:")
        print(stats.to_string(index=False))
        
        # Consulta por tipo de estado
        state_stats = pd.read_sql_query("""
            SELECT state_type, COUNT(*) as count 
            FROM corda_transactions 
            GROUP BY state_type 
            ORDER BY count DESC
        """, conn)
        
        print(f"\nDistribucion por tipo de estado:")
        print(state_stats.to_string(index=False))
        
        conn.close()
        print("\nOK: Base de datos verificada exitosamente")
        return True
        
    except Exception as e:
        print(f"ERROR: Error verificando base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    verify_database()
