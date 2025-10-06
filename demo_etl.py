#!/usr/bin/env python3
"""
Demo del ETL para Corda - Simulación completa
Demuestra el proceso ETL completo con datos simulados
"""

import json
import logging
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List
import random
import time

class CordaETLDemo:
    """Demo del ETL para Corda con simulación de datos"""
    
    def __init__(self):
        """Inicializar el demo del ETL"""
        self.setup_logging()
        self.logger.info("Demo ETL Corda inicializado")
    
    def setup_logging(self):
        """Configurar logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('demo_etl.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def simulate_connection_test(self) -> bool:
        """Simular prueba de conexión exitosa"""
        self.logger.info("Simulando conexion a Corda testnet...")
        time.sleep(1)  # Simular tiempo de conexión
        
        # Simular conexión exitosa
        self.logger.info("OK: Conexion exitosa a Corda testnet simulada")
        self.logger.info("Red: Corda Testnet Demo")
        return True
    
    def generate_sample_transactions(self, count: int = 50) -> List[Dict]:
        """Generar transacciones de muestra realistas"""
        self.logger.info(f"Generando {count} transacciones de muestra...")
        
        transactions = []
        base_time = datetime.now() - timedelta(days=7)
        
        for i in range(count):
            # Generar datos realistas
            transaction_time = base_time + timedelta(
                hours=random.randint(0, 168),  # Última semana
                minutes=random.randint(0, 59)
            )
            
            # Tipos de transacciones típicas de Corda
            transaction_types = [
                "IouState", "CashState", "CommercialPaperState", 
                "BondState", "EquityState", "LoanState"
            ]
            
            # Participantes típicos
            participants = [
                ["O=BankA,L=London,C=GB", "O=BankB,L=NewYork,C=US"],
                ["O=CorpA,L=Tokyo,C=JP", "O=CorpB,L=Berlin,C=DE"],
                ["O=TraderA,L=Singapore,C=SG", "O=TraderB,L=Zurich,C=CH"],
                ["O=ExchangeA,L=HongKong,C=HK", "O=ExchangeB,L=Frankfurt,C=DE"]
            ]
            
            transaction = {
                "id": f"tx_{i}_{int(transaction_time.timestamp())}",
                "timestamp": transaction_time.isoformat(),
                "type": "StateTransition",
                "state_type": random.choice(transaction_types),
                "participants": random.choice(participants),
                "amount": round(random.uniform(1000, 1000000), 2),
                "currency": random.choice(["USD", "EUR", "GBP", "JPY", "CHF"]),
                "status": random.choice(["CONFIRMED", "PENDING", "FAILED"]),
                "block_height": 1000 + i,
                "network": "corda_testnet_demo",
                "notary": f"O=Notary{i%3},L=London,C=GB",
                "contract": f"com.example.{random.choice(['iou', 'cash', 'bond'])}",
                "flow_id": f"flow_{i}_{random.randint(1000, 9999)}",
                "extraction_timestamp": datetime.now().isoformat()
            }
            
            transactions.append(transaction)
        
        self.logger.info(f"OK: Generadas {len(transactions)} transacciones de muestra")
        return transactions
    
    def transform_data(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Transformar datos a formato tabular"""
        self.logger.info("Transformando datos...")
        
        try:
            # Normalizar datos JSON a DataFrame
            df = pd.json_normalize(raw_data)
            
            # Limpiar y estructurar datos
            df['processed'] = True
            df['processing_timestamp'] = datetime.now().isoformat()
            
            # Convertir listas a strings para SQLite
            if 'participants' in df.columns:
                df['participants'] = df['participants'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
            
            # Convertir timestamp a datetime para análisis
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['extraction_timestamp'] = pd.to_datetime(df['extraction_timestamp'])
            
            self.logger.info(f"OK: Datos transformados: {len(df)} registros")
            return df
            
        except Exception as e:
            self.logger.error(f"Error transformando datos: {str(e)}")
            return pd.DataFrame()
    
    def load_to_database(self, df: pd.DataFrame) -> bool:
        """Cargar datos a base de datos SQLite"""
        self.logger.info("Cargando datos a base de datos...")
        
        try:
            conn = sqlite3.connect('demo_blockchain_data.db')
            
            # Crear tabla si no existe
            df.to_sql(
                'corda_transactions',
                conn,
                if_exists='replace',
                index=False
            )
            
            # Crear índices para consultas eficientes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON corda_transactions(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_state_type ON corda_transactions(state_type)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_status ON corda_transactions(status)")
            
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
            filename = f"demo_corda_data_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"OK: Datos guardados en {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Error guardando JSON: {str(e)}")
            return ""
    
    def generate_analytics_summary(self, df: pd.DataFrame) -> Dict:
        """Generar resumen analítico de los datos"""
        try:
            summary = {
                "total_transactions": len(df),
                "date_range": {
                    "start": df['timestamp'].min().isoformat(),
                    "end": df['timestamp'].max().isoformat()
                },
                "state_types": df['state_type'].value_counts().to_dict(),
                "currencies": df['currency'].value_counts().to_dict(),
                "status_distribution": df['status'].value_counts().to_dict(),
                "total_amount": df['amount'].sum(),
                "average_amount": df['amount'].mean(),
                "participants_count": len(df['participants'].explode().unique()),
                "generated_at": datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generando resumen: {str(e)}")
            return {}
    
    def run_demo_etl(self, transaction_count: int = 100):
        """Ejecutar demo completo del ETL"""
        self.logger.info("Iniciando demo ETL completo...")
        
        print("=" * 60)
        print("DEMO ETL PARA BLOCKCHAIN CORDA - TESTNET")
        print("=" * 60)
        
        # Paso 1: Simular conexión
        print("\n1. Probando conexion a Corda testnet...")
        if not self.simulate_connection_test():
            print("ERROR: No se pudo conectar")
            return False
        print("OK: Conexion exitosa")
        
        # Paso 2: Generar datos de muestra
        print("\n2. Generando datos de transacciones...")
        raw_transactions = self.generate_sample_transactions(transaction_count)
        print(f"OK: Generadas {len(raw_transactions)} transacciones")
        
        # Paso 3: Guardar JSON
        print("\n3. Guardando datos en formato JSON...")
        json_file = self.save_json_output(raw_transactions)
        print(f"OK: Archivo JSON creado: {json_file}")
        
        # Paso 4: Transformar datos
        print("\n4. Transformando datos...")
        df = self.transform_data(raw_transactions)
        if df.empty:
            print("ERROR: Error en transformacion")
            return False
        print(f"OK: Datos transformados: {len(df)} registros")
        
        # Paso 5: Cargar a base de datos
        print("\n5. Cargando datos a base de datos...")
        if not self.load_to_database(df):
            print("ERROR: Error cargando a base de datos")
            return False
        print("OK: Datos cargados a base de datos")
        
        # Paso 6: Generar análisis
        print("\n6. Generando resumen analitico...")
        summary = self.generate_analytics_summary(df)
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print("RESUMEN DEL PROCESO ETL")
        print("=" * 60)
        print(f"Total de transacciones: {summary.get('total_transactions', 0)}")
        print(f"Rango de fechas: {summary.get('date_range', {}).get('start', 'N/A')} a {summary.get('date_range', {}).get('end', 'N/A')}")
        print(f"Monto total: ${summary.get('total_amount', 0):,.2f}")
        print(f"Monto promedio: ${summary.get('average_amount', 0):,.2f}")
        print(f"Tipos de estado: {len(summary.get('state_types', {}))}")
        print(f"Monedas: {', '.join(summary.get('currencies', {}).keys())}")
        print(f"Participantes únicos: {summary.get('participants_count', 0)}")
        
        # Guardar resumen
        with open('etl_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("ARCHIVOS GENERADOS:")
        print("=" * 60)
        print(f"- {json_file} (datos en formato JSON)")
        print("- demo_blockchain_data.db (base de datos SQLite)")
        print("- etl_summary.json (resumen analitico)")
        print("- demo_etl.log (log del proceso)")
        
        print("\nOK: Demo ETL completado exitosamente!")
        return True

def main():
    """Función principal del demo"""
    demo = CordaETLDemo()
    success = demo.run_demo_etl(transaction_count=75)
    
    if success:
        print("\nEl sistema esta listo para el siguiente paso: Dashboard con IA")
    else:
        print("\nERROR: El demo fallo. Revisa los logs.")

if __name__ == "__main__":
    main()
