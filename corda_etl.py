#!/usr/bin/env python3
"""
ETL para datos de blockchain Corda
Extrae datos de una red testnet de Corda y los procesa en formato JSON
"""

import json
import logging
import requests
import pandas as pd
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import configparser
import time

class CordaETL:
    """Clase principal para el proceso ETL de Corda"""
    
    def __init__(self, config_file: str = "config.ini"):
        """Inicializar el ETL con configuración"""
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # Configurar logging
        self.setup_logging()
        
        # URLs y configuración de red
        self.node_url = self.config.get('NETWORK', 'node_url')
        self.api_endpoint = self.config.get('API', 'api_endpoint')
        self.timeout = self.config.getint('API', 'timeout')
        self.retry_attempts = self.config.getint('API', 'retry_attempts')
        
        # Base de datos
        self.db_path = self.config.get('DATABASE', 'db_path')
        
        self.logger.info("ETL Corda inicializado correctamente")
    
    def setup_logging(self):
        """Configurar el sistema de logging"""
        log_level = self.config.get('LOGGING', 'log_level')
        log_file = self.config.get('LOGGING', 'log_file')
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def test_connection(self) -> bool:
        """Probar la conexión a la red testnet de Corda"""
        self.logger.info("Iniciando prueba de conexión a Corda testnet...")
        
        try:
            # Intentar conectar a la API de Corda
            response = requests.get(
                f"{self.api_endpoint}/network/map",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                self.logger.info("OK: Conexion exitosa a Corda testnet")
                network_data = response.json()
                self.logger.info(f"Red: {network_data.get('networkName', 'N/A')}")
                return True
            else:
                self.logger.error(f"ERROR: Error de conexion: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"ERROR: Error de conexion: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"ERROR: Error inesperado: {str(e)}")
            return False
    
    def get_network_info(self) -> Dict:
        """Obtener información de la red"""
        try:
            response = requests.get(
                f"{self.api_endpoint}/network/map",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Error obteniendo info de red: {response.status_code}")
                return {}
        except Exception as e:
            self.logger.error(f"Error obteniendo info de red: {str(e)}")
            return {}
    
    def get_node_info(self) -> Dict:
        """Obtener información del nodo"""
        try:
            response = requests.get(
                f"{self.api_endpoint}/network/map",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                network_data = response.json()
                nodes = network_data.get('nodes', [])
                if nodes:
                    return nodes[0]  # Retornar primer nodo disponible
            return {}
        except Exception as e:
            self.logger.error(f"Error obteniendo info del nodo: {str(e)}")
            return {}
    
    def extract_transactions(self, limit: int = 100) -> List[Dict]:
        """Extraer transacciones de la blockchain"""
        self.logger.info(f"Extrayendo {limit} transacciones...")
        
        transactions = []
        try:
            # Simular extracción de transacciones (en una implementación real,
            # esto se conectaría a la API específica de Corda)
            for i in range(limit):
                # Crear transacción simulada con estructura típica de Corda
                transaction = {
                    "id": f"tx_{i}_{int(time.time())}",
                    "timestamp": datetime.now().isoformat(),
                    "type": "StateTransition",
                    "participants": [
                        f"O=PartyA,L=London,C=GB",
                        f"O=PartyB,L=NewYork,C=US"
                    ],
                    "state_type": "IouState",
                    "amount": 1000 + (i * 100),
                    "currency": "USD",
                    "status": "CONFIRMED",
                    "block_height": 1000 + i,
                    "network": "corda_testnet"
                }
                transactions.append(transaction)
            
            self.logger.info(f"OK: Extraidas {len(transactions)} transacciones")
            return transactions
            
        except Exception as e:
            self.logger.error(f"Error extrayendo transacciones: {str(e)}")
            return []
    
    def transform_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Transformar datos a formato tabular"""
        self.logger.info("Transformando datos...")
        
        try:
            # Normalizar datos JSON a DataFrame
            df = pd.json_normalize(raw_data)
            
            # Limpiar y estructurar datos
            df['extraction_timestamp'] = datetime.now().isoformat()
            df['processed'] = True
            
            self.logger.info(f"OK: Datos transformados: {len(df)} registros")
            return df
            
        except Exception as e:
            self.logger.error(f"Error transformando datos: {str(e)}")
            return pd.DataFrame()
    
    def load_to_database(self, df: pd.DataFrame) -> bool:
        """Cargar datos a base de datos SQLite"""
        self.logger.info("Cargando datos a base de datos...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Crear tabla si no existe
            df.to_sql(
                self.config.get('DATABASE', 'table_name'),
                conn,
                if_exists='replace',
                index=False
            )
            
            conn.close()
            self.logger.info("OK: Datos cargados a base de datos")
            return True
            
        except Exception as e:
            self.logger.error(f"Error cargando datos: {str(e)}")
            return False
    
    def save_json_output(self, data: List[Dict], filename: str = None) -> str:
        """Guardar datos en formato JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"corda_data_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"OK: Datos guardados en {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error guardando JSON: {str(e)}")
            return ""
    
    def run_etl_process(self, transaction_limit: int = 100):
        """Ejecutar proceso ETL completo"""
        self.logger.info("Iniciando proceso ETL completo...")
        
        # Paso 1: Probar conexión
        if not self.test_connection():
            self.logger.error("ERROR: No se pudo conectar a la red. Abortando ETL.")
            return False
        
        # Paso 2: Obtener información de red
        network_info = self.get_network_info()
        node_info = self.get_node_info()
        
        # Paso 3: Extraer datos
        raw_transactions = self.extract_transactions(transaction_limit)
        if not raw_transactions:
            self.logger.error("ERROR: No se pudieron extraer datos")
            return False
        
        # Paso 4: Guardar JSON
        json_file = self.save_json_output(raw_transactions)
        
        # Paso 5: Transformar datos
        df = self.transform_data(raw_transactions)
        if df.empty:
            self.logger.error("ERROR: Error en transformacion de datos")
            return False
        
        # Paso 6: Cargar a base de datos
        if not self.load_to_database(df):
            self.logger.error("ERROR: Error cargando a base de datos")
            return False
        
        self.logger.info("OK: Proceso ETL completado exitosamente")
        return True

def main():
    """Función principal"""
    print("ETL para Blockchain Corda - Testnet")
    print("=" * 50)
    
    # Crear instancia del ETL
    etl = CordaETL()
    
    # Ejecutar proceso ETL
    success = etl.run_etl_process(transaction_limit=50)
    
    if success:
        print("\nOK: Proceso ETL completado exitosamente")
        print("Archivos generados:")
        print("   - corda_data_*.json (datos en formato JSON)")
        print("   - blockchain_data.db (base de datos SQLite)")
        print("   - etl_corda.log (log del proceso)")
    else:
        print("\nERROR: El proceso ETL fallo. Revisa los logs para mas detalles.")

if __name__ == "__main__":
    main()
