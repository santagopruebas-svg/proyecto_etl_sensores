import os
import json
import shutil
from src.extract import encontrar_archivos_por_procesar, leer_archivo_excel
from src.transform import limpiar_y_estandarizar
from src.load import guardar_datos_transformados

# Nota: Ya no importamos COLUMNAS_SALIDA fijo, porque ahora es dinámico.

def cargar_configuracion_rutas(config_file="config.json"):
    """Carga las rutas desde el archivo JSON de configuración."""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR Config: {e}")
        return None

def mover_a_archivados(filepath, carpeta_base_archivados, subcarpeta):
    """
    Mueve el archivo a Archive/Subcarpeta (ej: Archive/Pasillos/)
    Sobrescribe si el archivo ya existe en el destino.
    """
    try:
        destino_folder = os.path.join(carpeta_base_archivados, subcarpeta)
        os.makedirs(destino_folder, exist_ok=True)
        
        filename = os.path.basename(filepath)
        destino_path = os.path.join(destino_folder, filename)
        
        # Si existe, lo borramos para poder mover el nuevo
        if os.path.exists(destino_path):
            os.remove(destino_path)
            
        shutil.move(filepath, destino_path)
        # print(f"   -> Archivado en: {subcarpeta}") 
    except Exception as e:
        print(f"ERROR al archivar {filepath}: {e}")

def main():
    print("==================================================")
    print("       INICIO DEL PROCESO ETL (MULTI-SCHEMA)      ")
    print("==================================================")

    config = cargar_configuracion_rutas()
    if not config: return

    # Rutas generales
    OUT_DIR_GENERAL = config.get("CARPETA_DESTINO_GENERAL")
    ARCHIVE_DIR_GENERAL = config.get("CARPETA_ARCHIVADOS_GENERAL")
    PROCESOS = config.get("RUTAS_PROCESO", {})

    if not PROCESOS:
        print("ADVERTENCIA: No se encontraron procesos definidos en 'RUTAS_PROCESO'.")
        return

    # Iterar sobre cada proceso configurado (PASILLOS, PRESION, COMPRESORES, etc.)
    for nombre_proceso, rutas in PROCESOS.items():
        print(f"\n>>> PROCESANDO GRUPO: {nombre_proceso}")
        
        input_folder = rutas.get("INPUT")
        output_filename = rutas.get("OUTPUT_NAME")
        
        # Validaciones básicas
        if not input_folder or not os.path.exists(input_folder):
            print(f"   Advertencia: Carpeta de entrada no existe o no definida: {input_folder}")
            continue

        archivos = encontrar_archivos_por_procesar(input_folder)
        
        if not archivos:
            print("   No hay archivos nuevos para procesar.")
            continue

        buffer_proceso = []
        schema_header_to_use = None # Aquí guardaremos la cabecera correcta para este lote

        for filepath in archivos:
            filename = os.path.basename(filepath)
            
            # 1. Extracción
            # leer_archivo_excel cierra el archivo automáticamente ahora
            headers, data_rows, conf = leer_archivo_excel(filepath)
            
            if not data_rows or not conf:
                print(f"   [SALTADO] {filename} (No se identificó config o está vacío)")
                continue
            
            # 2. Transformación
            # Ahora devuelve una TUPLA: (Filas_Limpias, Cabecera_Usada)
            resultado = limpiar_y_estandarizar(headers, data_rows, conf)
            
            if resultado:
                cleaned_rows, current_schema_header = resultado
                
                # Acumular filas
                buffer_proceso.extend(cleaned_rows)
                
                # Capturar la cabecera (Asumimos que todos los archivos de esta carpeta usan el mismo esquema)
                schema_header_to_use = current_schema_header
                
                # 3. Archivado
                mover_a_archivados(filepath, ARCHIVE_DIR_GENERAL, nombre_proceso.capitalize())
                print(f"   [OK] {filename}")
            else:
                print(f"   [FALLO TRANSFORMACIÓN] {filename}")

        # 4. Carga (Guardar CSV consolidado del proceso)
        if buffer_proceso and schema_header_to_use:
            # Construimos la data final: Cabecera + Filas
            full_data = [schema_header_to_use] + buffer_proceso
            
            guardar_datos_transformados(full_data, OUT_DIR_GENERAL, output_filename)
            print(f"   -> ÉXITO: Se generó {output_filename} con {len(buffer_proceso)} registros.")
        else:
            print(f"   -> FINALIZADO: No se generaron datos válidos para {nombre_proceso}.")

    print("\n==================================================")
    print("             PROCESO ETL FINALIZADO               ")
    print("==================================================")

if __name__ == "__main__":
    main()