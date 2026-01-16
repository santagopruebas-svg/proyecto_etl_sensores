# src/transform.py
from datetime import datetime, timedelta

def redondear_hora_10min(dt):
    """Redondea al intervalo de 10 min más cercano."""
    minutos = dt.minute
    residuo = minutos % 10
    
    if residuo < 5:
        minutos_redondeados = minutos - residuo
    else:
        minutos_redondeados = minutos + (10 - residuo)
    
    dt_base = dt.replace(second=0, microsecond=0)
    
    if minutos_redondeados == 60:
        return (dt_base.replace(minute=0) + timedelta(hours=1)).strftime('%H:%M')
    else:
        return dt_base.replace(minute=minutos_redondeados).strftime('%H:%M')

def generar_llave_comun(anio, mes, dia, hora_10min):
    """Genera una llave única concatenando los valores de tiempo."""
    if any(v is None for v in [anio, mes, dia, hora_10min]):
        return None
    # Formato: YYYYMMDDHHMM (sin dos puntos para que sea puro texto/número)
    # Ejemplo: 2026 + 01 + 16 + 00:10 -> "202601160010"
    
    # Limpiar la hora de los dos puntos ':' para la llave
    hora_limpia = str(hora_10min).replace(':', '')
    
    # Asegurar dos dígitos para mes y día
    return f"{anio}{int(mes):02d}{int(dia):02d}{hora_limpia}"

def estandarizar_codigo_pasillo(nombre_original):
    """
    Transforma el nombre del pasillo en un código estandarizado (P001, P010, etc).
    """
    if not nombre_original:
        return None
        
    nombre_upper = str(nombre_original).upper().strip()
    
    # Regla 1: Pulmón
    if "PULM" in nombre_upper: # Captura "Pulmón", "Pulmon"
        return "PULMON"
    
    # Regla 2: Pasillo 18 (y sus variantes RS) -> P018
    if "PASILLO" in nombre_upper and "18" in nombre_upper:
        return "P018"
        
    # Regla 3: Pasillos numerados (Pasillo 1 ... Pasillo 10)
    if "PASILLO" in nombre_upper:
        try:
            # Extraer números del string
            numeros = [int(s) for s in nombre_upper.split() if s.isdigit()]
            if numeros:
                # Tomamos el primer número encontrado
                numero = numeros[0]
                # Formatear a 3 dígitos (P001, P010, P100)
                return f"P{numero:03d}"
        except:
            pass # Si falla, devuelve el original abajo
            
    # Caso por defecto (Muelles, Túneles o no reconocidos): Se devuelve el nombre original
    return nombre_original

def limpiar_y_estandarizar(original_headers, data_rows, config):
    # 1. Obtener Esquema
    SCHEMA_COLUMNS = config['output_schema']
    SCHEMA_INDICES = {col: i for i, col in enumerate(SCHEMA_COLUMNS)}
    
    idx_map = {}
    mapping = config['column_mapping']
    
    for original_col_name, standard_col_name in mapping.items():
        try:
            original_idx = original_headers.index(original_col_name)
            standard_idx = SCHEMA_INDICES[standard_col_name]
            idx_map[original_idx] = standard_idx
        except ValueError:
            pass 
        except KeyError:
             print(f"Error Config: Columna destino '{standard_col_name}' no existe.")
             return None

    id_col_name = config.get('id_column_name')
    id_standard_idx = SCHEMA_INDICES.get(id_col_name)
    nombre_identificador = config.get('nombre_identificador')
    
    # Pre-calcular el código estandarizado si corresponde (solo para Sensores)
    codigo_estandarizado = None
    if 'Pasillo_est' in SCHEMA_INDICES:
        codigo_estandarizado = estandarizar_codigo_pasillo(nombre_identificador)

    processed_rows = []
    
    for row in data_rows:
        standard_row = [None] * len(SCHEMA_COLUMNS)
        
        # Insertar Identificador
        if id_standard_idx is not None:
            standard_row[id_standard_idx] = nombre_identificador
            
        # Insertar Código Estandarizado (si existe la columna en el esquema)
        if codigo_estandarizado and 'Pasillo_est' in SCHEMA_INDICES:
            standard_row[SCHEMA_INDICES['Pasillo_est']] = codigo_estandarizado

        # Copiar datos
        for original_idx, standard_idx in idx_map.items():
            if original_idx < len(row):
                val = row[original_idx]
                if val is not None and not (isinstance(val, str) and val.strip() == ''):
                    standard_row[standard_idx] = val
        
        # --- FECHAS Y LLAVE COMÚN ---
        idx_fecha_orig = SCHEMA_INDICES.get('FechaHora_Original')
        
        anio, mes, dia, hora10 = None, None, None, None
        
        if idx_fecha_orig is not None:
            val_fecha = standard_row[idx_fecha_orig]
            dt_obj = None
            if val_fecha:
                try:
                    if isinstance(val_fecha, datetime):
                        dt_obj = val_fecha
                    elif isinstance(val_fecha, str):
                        str_fecha = val_fecha.strip()
                        try: dt_obj = datetime.strptime(str_fecha, '%d/%m/%Y %H:%M')
                        except ValueError:
                            try: dt_obj = datetime.strptime(str_fecha, '%d/%m/%Y %H:%M:%S')
                            except ValueError: 
                                try: dt_obj = datetime.strptime(str_fecha, '%Y-%m-%d %H:%M:%S')
                                except ValueError: pass
                    
                    if dt_obj:
                        anio = dt_obj.year
                        mes = dt_obj.month
                        dia = dt_obj.day
                        hora10 = redondear_hora_10min(dt_obj)
                        
                        # Asignar a columnas
                        if 'Anio' in SCHEMA_INDICES: standard_row[SCHEMA_INDICES['Anio']] = anio
                        if 'Mes' in SCHEMA_INDICES: standard_row[SCHEMA_INDICES['Mes']] = mes
                        if 'Dia' in SCHEMA_INDICES: standard_row[SCHEMA_INDICES['Dia']] = dia
                        if 'Hora_10min' in SCHEMA_INDICES: standard_row[SCHEMA_INDICES['Hora_10min']] = hora10
                        
                except Exception:
                    pass

        # --- GENERAR LLAVE COMÚN ---
        # Se genera solo si tenemos los datos de fecha completos
        if 'Llave_Comun' in SCHEMA_INDICES:
            llave = generar_llave_comun(anio, mes, dia, hora10)
            standard_row[SCHEMA_INDICES['Llave_Comun']] = llave

        # --- CONVERSIÓN NUMÉRICA ---
        numeric_fields = config.get('numeric_fields', [])
        for col_name in numeric_fields:
            idx = SCHEMA_INDICES.get(col_name)
            if idx is not None:
                val = standard_row[idx]
                if val is not None:
                    try:
                        if isinstance(val, (int, float)):
                            standard_row[idx] = float(val)
                        elif isinstance(val, str):
                            clean = val.strip().replace(',', '.')
                            standard_row[idx] = float(clean) if clean and clean.lower() != 'nan' else None
                    except ValueError:
                        standard_row[idx] = None

        processed_rows.append(standard_row)

    return (processed_rows, SCHEMA_COLUMNS) if processed_rows else None