#!/usr/bin/env python3
"""
Generador Incremental de Datos
Continúa desde donde se quedó y maneja desconexiones
"""

import psycopg2
import random
import uuid
import json
from datetime import datetime, timedelta
import time

def generar_datos_incremental():
    """Generar datos incrementales hasta llegar a 100,000"""
    
    print("=" * 80)
    print("🚀 GENERADOR INCREMENTAL DE DATOS")
    print("=" * 80)
    print()
    
    # Configuración de base de datos
    db_config = {
        'host': 'dpg-d3hk1u33fgac739s7s9g-a.oregon-postgres.render.com',
        'port': 5432,
        'database': 'blokchain_bd',
        'user': 'blokchain_bd_user',
        'password': 'RlxkDsSrWcte8ASrxsztagJWod7qNrWP'
    }
    
    # Configuración de datos
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'BRL', 'MXN']
    state_types = [
        'CashState', 'CommercialPaper', 'IOUState', 'LoanState', 'BondState',
        'StockState', 'CommodityState', 'RealEstateState', 'InsuranceState', 'DerivativeState'
    ]
    statuses = ['CONFIRMED', 'PENDING', 'FAILED', 'CANCELLED']
    networks = ['CordaNetwork', 'TestNetwork', 'MainNetwork']
    notaries = ['NotaryA', 'NotaryB', 'NotaryC', 'NotaryD']
    contracts = [
        'CashContract', 'CommercialPaperContract', 'IOUContract', 'LoanContract',
        'BondContract', 'StockContract', 'CommodityContract', 'RealEstateContract'
    ]
    
    def conectar_bd_con_reintentos():
        """Conectar con reintentos automáticos"""
        max_intentos = 5
        for intento in range(max_intentos):
            try:
                conn = psycopg2.connect(**db_config)
                conn.autocommit = False
                return conn
            except Exception as e:
                print(f"⚠️ Intento {intento + 1} fallido: {str(e)}")
                if intento < max_intentos - 1:
                    wait_time = (intento + 1) * 5
                    print(f"   ⏳ Esperando {wait_time} segundos antes de reintentar...")
                    time.sleep(wait_time)
                else:
                    print("❌ No se pudo conectar después de varios intentos")
                    return None
    
    def verificar_datos_actuales():
        """Verificar cuántas transacciones hay actualmente"""
        conn = conectar_bd_con_reintentos()
        if not conn:
            return 0, 0
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), MAX(id) FROM corda_transactions")
            result = cursor.fetchone()
            count = result[0] if result[0] else 0
            max_id = result[1] if result[1] else 0
            conn.close()
            return count, max_id
        except Exception as e:
            print(f"❌ Error verificando datos: {str(e)}")
            if conn:
                conn.close()
            return 0, 0
    
    def generar_timestamp_realista(start_date, end_date):
        """Generar timestamp con patrones realistas"""
        base_time = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        
        # Patrones de actividad
        hour = base_time.hour
        is_weekday = base_time.weekday() < 5
        
        # Horario laboral (9-17) en días de semana - alta actividad
        if 9 <= hour <= 17 and is_weekday:
            if random.random() < 0.8:
                return base_time
        # Tarde/noche (18-22) - actividad media
        elif 18 <= hour <= 22:
            if random.random() < 0.4:
                return base_time
        # Noche/madrugada (23-8) - baja actividad
        elif hour >= 23 or hour <= 8:
            if random.random() < 0.1:
                return base_time
        # Fin de semana - actividad reducida
        elif not is_weekday:
            if random.random() < 0.2:
                return base_time
        
        # Si no cumple patrones, usar aleatorio simple
        return start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
    
    def generar_transaccion(tx_id, timestamp):
        """Generar una transacción individual"""
        currency = random.choice(currencies)
        
        # Generar monto realista
        rand = random.random()
        if rand < 0.4:
            amount = random.uniform(10, 1000)
        elif rand < 0.75:
            amount = random.uniform(1000, 10000)
        elif rand < 0.95:
            amount = random.uniform(10000, 100000)
        else:
            amount = random.uniform(100000, 1000000)
        
        # Ajustar según moneda
        if currency in ['JPY', 'KRW']:
            amount *= 100
        elif currency in ['BRL', 'MXN']:
            amount *= 5
        
        # Generar participantes
        num_participants = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
        participants = []
        for i in range(num_participants):
            participants.append({
                'name': f'Participant_{i+1}',
                'org': f'Org_{random.randint(1, 100)}',
                'role': random.choice(['Issuer', 'Holder', 'Verifier'])
            })
        
        return {
            'id': f'corda_tx_{tx_id}_{int(timestamp.timestamp())}',
            'timestamp': timestamp,
            'state_type': random.choice(state_types),
            'participants': json.dumps(participants),
            'amount': str(round(amount, 2)),
            'currency': currency,
            'status': random.choices(
                statuses, 
                weights=[0.85, 0.10, 0.03, 0.02]
            )[0],
            'block_height': random.randint(1000, 50000),
            'network': random.choice(networks),
            'notary': random.choice(notaries),
            'contract': random.choice(contracts),
            'flow_id': str(uuid.uuid4()),
            'extraction_timestamp': timestamp + timedelta(seconds=random.randint(1, 300)),
            'processed': random.choice([True, False]),
            'processing_timestamp': timestamp + timedelta(seconds=random.randint(1, 600))
        }
    
    def insertar_lote_seguro(transacciones, lote_num):
        """Insertar lote de manera segura con reintentos"""
        max_intentos = 3
        
        for intento in range(max_intentos):
            conn = None
            try:
                conn = conectar_bd_con_reintentos()
                if not conn:
                    raise Exception("No se pudo conectar a la base de datos")
                
                cursor = conn.cursor()
                
                # Query de inserción
                insert_query = """
                INSERT INTO corda_transactions (
                    id, timestamp, state_type, participants, amount, currency, 
                    status, block_height, network, notary, contract, flow_id,
                    extraction_timestamp, processed, processing_timestamp
                ) VALUES (
                    %(id)s, %(timestamp)s, %(state_type)s, %(participants)s, %(amount)s, %(currency)s,
                    %(status)s, %(block_height)s, %(network)s, %(notary)s, %(contract)s, %(flow_id)s,
                    %(extraction_timestamp)s, %(processed)s, %(processing_timestamp)s
                )
                """
                
                # Insertar en sub-lotes de 500 para mayor estabilidad
                sub_batch_size = 500
                for i in range(0, len(transacciones), sub_batch_size):
                    sub_batch = transacciones[i:i + sub_batch_size]
                    cursor.executemany(insert_query, sub_batch)
                    conn.commit()
                
                conn.close()
                print(f"   ✅ Lote {lote_num} insertado exitosamente - {len(transacciones):,} transacciones")
                return True
                
            except Exception as e:
                if conn:
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                
                print(f"⚠️ Error en lote {lote_num}, intento {intento + 1}: {str(e)}")
                if intento < max_intentos - 1:
                    wait_time = (intento + 1) * 10
                    print(f"   ⏳ Esperando {wait_time} segundos antes de reintentar...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ Falló definitivamente el lote {lote_num}")
                    return False
        
        return False
    
    try:
        # Verificar estado actual
        print("🔍 Verificando estado actual de la base de datos...")
        count_actual, max_id = verificar_datos_actuales()
        
        print(f"📊 Transacciones actuales: {count_actual:,}")
        print(f"🆔 Último ID: {max_id}")
        
        if count_actual >= 100000:
            print("🎉 ¡Ya tienes 100,000+ transacciones! No es necesario generar más.")
            return True
        
        faltantes = 100000 - count_actual
        print(f"📈 Transacciones faltantes: {faltantes:,}")
        print()
        
        # Configurar fechas
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * 3)  # 3 años atrás
        
        print(f"📅 Período: {start_date.date()} a {end_date.date()}")
        print()
        
        # Generar en lotes pequeños de 2,000
        lote_size = 2000
        total_lotes = (faltantes + lote_size - 1) // lote_size
        
        print(f"📦 Tamaño de lote: {lote_size:,}")
        print(f"🔢 Lotes a generar: {total_lotes}")
        print()
        
        start_time = time.time()
        transacciones_insertadas = 0
        # Extraer número del ID para continuar
        if max_id and 'corda_tx_' in str(max_id):
            try:
                # Extraer el número del ID (ej: corda_tx_9999_1746381657 -> 9999)
                parts = str(max_id).split('_')
                if len(parts) >= 3:
                    start_id = int(parts[2]) + 1
                else:
                    start_id = 23500 + 1
            except:
                start_id = 23500 + 1
        else:
            start_id = 23500 + 1
        
        for lote_num in range(1, total_lotes + 1):
            # Calcular tamaño del lote actual
            remaining = faltantes - transacciones_insertadas
            current_lote_size = min(lote_size, remaining)
            
            print(f"🔄 Generando lote {lote_num}/{total_lotes} ({current_lote_size:,} transacciones)...")
            
            # Generar lote
            transacciones = []
            for i in range(current_lote_size):
                tx_id = start_id + i
                timestamp = generar_timestamp_realista(start_date, end_date)
                tx = generar_transaccion(tx_id, timestamp)
                transacciones.append(tx)
            
            # Insertar lote
            if insertar_lote_seguro(transacciones, lote_num):
                transacciones_insertadas += current_lote_size
                start_id += current_lote_size
                
                # Verificar progreso
                total_actual = count_actual + transacciones_insertadas
                progress = (total_actual / 100000) * 100
                print(f"   📊 Progreso total: {total_actual:,}/100,000 ({progress:.1f}%)")
                
                # Pausa entre lotes para no sobrecargar
                if lote_num < total_lotes:
                    print(f"   ⏸️ Pausa de 5 segundos...")
                    time.sleep(5)
            else:
                print(f"❌ Error crítico en lote {lote_num}. Deteniendo.")
                break
        
        total_time = time.time() - start_time
        
        # Verificar resultado final
        count_final, _ = verificar_datos_actuales()
        
        print()
        print("=" * 80)
        print("🎉 GENERACIÓN INCREMENTAL COMPLETADA")
        print("=" * 80)
        print(f"📊 Transacciones insertadas en esta sesión: {transacciones_insertadas:,}")
        print(f"📊 Total en base de datos: {count_final:,}")
        print(f"📊 Objetivo: 100,000")
        print(f"🕐 Tiempo total: {total_time/60:.2f} minutos")
        if transacciones_insertadas > 0:
            print(f"📈 Velocidad promedio: {transacciones_insertadas/total_time:.0f} transacciones/segundo")
        
        if count_final >= 100000:
            print()
            print("🚀 ¡ÉXITO! Has alcanzado los 100,000+ transacciones")
            print("🔄 El dashboard ahora tiene datos suficientes para análisis completo")
            return True
        elif count_final >= 50000:
            print()
            print("✅ ¡Buen progreso! Tienes datos suficientes para análisis")
            print(f"💡 Para llegar a 100k, ejecuta este script nuevamente")
            return True
        else:
            print()
            print("⚠️ Se generaron pocas transacciones. Revisa la conexión.")
            print(f"💡 Ejecuta este script nuevamente para continuar")
            return False
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    generar_datos_incremental()
