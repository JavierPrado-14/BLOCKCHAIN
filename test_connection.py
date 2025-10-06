#!/usr/bin/env python3
"""
Script de prueba de conexión a Corda testnet
Valida la conectividad y configuración del ETL
"""

import sys
import json
from corda_etl import CordaETL

def test_corda_connection():
    """Probar conexión a Corda y mostrar información de red"""
    print("Probando conexion a Corda Testnet")
    print("=" * 50)
    
    # Crear instancia del ETL
    etl = CordaETL()
    
    # Probar conexión básica
    print("\n1. Probando conexión básica...")
    connection_ok = etl.test_connection()
    
    if not connection_ok:
        print("ERROR: No se pudo conectar a la red testnet")
        print("Verificaciones sugeridas:")
        print("   - Verificar configuracion en config.ini")
        print("   - Comprobar conectividad a internet")
        print("   - Validar URL de la red testnet")
        return False
    
    # Obtener información de red
    print("\n2. Obteniendo información de red...")
    network_info = etl.get_network_info()
    
    if network_info:
        print("OK: Informacion de red obtenida:")
        print(f"   - Nombre de red: {network_info.get('networkName', 'N/A')}")
        print(f"   - Nodos disponibles: {len(network_info.get('nodes', []))}")
    else:
        print("WARNING: No se pudo obtener informacion detallada de la red")
    
    # Obtener información del nodo
    print("\n3. Obteniendo información del nodo...")
    node_info = etl.get_node_info()
    
    if node_info:
        print("OK: Informacion del nodo obtenida:")
        print(f"   - ID del nodo: {node_info.get('id', 'N/A')}")
        print(f"   - Estado: {node_info.get('status', 'N/A')}")
    else:
        print("WARNING: No se pudo obtener informacion del nodo")
    
    # Probar extracción de datos
    print("\n4. Probando extracción de datos...")
    sample_transactions = etl.extract_transactions(limit=5)
    
    if sample_transactions:
        print(f"OK: Extraidas {len(sample_transactions)} transacciones de prueba")
        print("Estructura de datos:")
        print(json.dumps(sample_transactions[0], indent=2))
    else:
        print("ERROR: No se pudieron extraer datos de prueba")
        return False
    
    print("\n" + "=" * 50)
    print("OK: Prueba de conexion completada exitosamente")
    print("El sistema esta listo para el proceso ETL completo")
    
    return True

def show_system_info():
    """Mostrar información del sistema y configuración"""
    print("\nInformacion del Sistema")
    print("-" * 30)
    
    try:
        import pandas as pd
        import requests
        import sqlite3
        
        print(f"OK: Python: {sys.version}")
        print(f"OK: Pandas: {pd.__version__}")
        print(f"OK: Requests: {requests.__version__}")
        print(f"OK: SQLite3: {sqlite3.sqlite_version}")
        
    except ImportError as e:
        print(f"ERROR: Error importando dependencias: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Sistema de Pruebas - ETL Corda")
    print("=" * 50)
    
    # Mostrar información del sistema
    if not show_system_info():
        print("ERROR: Error en dependencias del sistema")
        sys.exit(1)
    
    # Probar conexión
    if test_corda_connection():
        print("\nSistema listo para usar!")
    else:
        print("\nERROR: Sistema no esta listo. Revisa la configuracion.")
        sys.exit(1)
