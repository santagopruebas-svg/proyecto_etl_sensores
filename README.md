# 🏭 Proyecto ETL Sensores: Unificación de Datos (Multi-Esquema)

--------------------------------------------
**© 2026 IceStar Latam - Todos los derechos reservados**

* **Autor:** Daniel Andrés Dávila Lesmes
* **Rol:** Excelencia Operacional
* **Contacto:** danielandresd998@gmail.com
--------------------------------------------

## 📄 Descripción del Proyecto

Este proyecto implementa una arquitectura **ETL (Extracción, Transformación, Carga)** modular y robusta diseñada para unificar datos operativos provenientes de múltiples fuentes de archivos Excel con estructuras heterogéneas.

El sistema estandariza la información de:
1.  **Sensores:** Pasillos, Muelles, Túneles (Temperaturas, Setpoints, Estados).
2.  **Presión del Sistema:** Succión, Descarga, Aceite.
3.  **Compresores:** Estados de conexión/desconexión y alarmas.

El resultado son archivos **CSV limpios y consolidados**, optimizados con llaves relacionales para su ingesta directa en **Power BI**.

> **Nota Técnica:** Este proyecto está optimizado para entornos con restricciones. **NO utiliza `pandas`** ni dependencias pesadas. Se basa exclusivamente en `openpyxl` y la librería estándar de Python para máxima portabilidad y velocidad.

---

## 🚀 Arquitectura del Proyecto

El código sigue un diseño de **Separación de Responsabilidades**:

* **`config.json`**: Archivo maestro de configuración. Define las rutas de entrada/salida separadas por proceso (Pasillos, Presión, etc.).
* **`src/config.py`**: El "Cerebro" del sistema. Contiene:
    * Los esquemas de salida dinámicos (columnas específicas para Sensores vs Presión).
    * Los diccionarios de mapeo de columnas.
    * La lista de nombres internos para identificar archivos automáticamente.
* **`src/extract.py`**: Lee los archivos `.xlsx` usando `openpyxl` en modo lectura (`read_only`) para eficiencia de memoria. Cierra los archivos inmediatamente para permitir su movimiento.
* **`src/transform.py`**:
    * Limpia datos y convierte tipos numéricos.
    * **Genera `Llave_Comun`**: (YYYYMMDDHHMM) para relacionar tablas.
    * **Estandariza Fechas**: Redondea tiempos a intervalos de 10 minutos.
    * **Codifica Pasillos**: Transforma "Pasillo 1" a "P001".
* **`src/load.py`**: Genera los CSVs consolidados y maneja la escritura segura.
* **`run_etl.py`**: El orquestador. Itera sobre los procesos configurados, gestiona el flujo de datos y mueve los archivos procesados a la carpeta `Archive`.

---

## 📂 Estructura de Directorios

El sistema requiere una estructura de carpetas específica para separar los insumos por tipo de proceso.

```text
Carpeta Raiz/ (Configurable)
├── Archive/                  # Destino de archivos procesados
│   ├── Pasillos/
│   ├── Muelles/
│   ├── Tuneles/
│   ├── Presion/
│   └── Compresores/
│
├── Export/                   # Salida de CSVs limpios
│   ├── consol_pasillos.csv
│   ├── consol_muelles.csv
│   ├── consol_tuneles.csv
│   ├── consol_presion.csv
│   └── consol_compresores.csv
│
├── Import/                   # Bandeja de entrada (Archivos .xlsx)
│   ├── Pasillos/
│   ├── Muelles/
│   ├── Tuneles/
│   ├── Presion/
│   └── Compresores/


Aquí tienes el contenido completo y definitivo del archivo README.md en un solo bloque de texto plano. Solo tienes que copiarlo y pegarlo en tu editor.

Markdown

# 🏭 Proyecto ETL Sensores: Unificación de Datos (Multi-Esquema)

--------------------------------------------
**© 2026 IceStar Latam - Todos los derechos reservados**

* **Autor:** Daniel Andrés Dávila Lesmes
* **Rol:** Excelencia Operacional
* **Contacto:** danielandresd998@gmail.com
--------------------------------------------

## 📄 Descripción del Proyecto

Este proyecto implementa una arquitectura **ETL (Extracción, Transformación, Carga)** modular y robusta diseñada para unificar datos operativos provenientes de múltiples fuentes de archivos Excel con estructuras heterogéneas.

El sistema estandariza la información de:
1.  **Sensores:** Pasillos, Muelles, Túneles (Temperaturas, Setpoints, Estados).
2.  **Presión del Sistema:** Succión, Descarga, Aceite.
3.  **Compresores:** Estados de conexión/desconexión y alarmas.

El resultado son archivos **CSV limpios y consolidados**, optimizados con llaves relacionales para su ingesta directa en **Power BI**.

> **Nota Técnica:** Este proyecto está optimizado para entornos con restricciones. **NO utiliza `pandas`** ni dependencias pesadas. Se basa exclusivamente en `openpyxl` y la librería estándar de Python para máxima portabilidad y velocidad.

---

## 🚀 Arquitectura del Proyecto

El código sigue un diseño de **Separación de Responsabilidades**:

* **`config.json`**: Archivo maestro de configuración. Define las rutas de entrada/salida separadas por proceso (Pasillos, Presión, etc.).
* **`src/config.py`**: El "Cerebro" del sistema. Contiene:
    * Los esquemas de salida dinámicos (columnas específicas para Sensores vs Presión).
    * Los diccionarios de mapeo de columnas.
    * La lista de nombres internos para identificar archivos automáticamente.
* **`src/extract.py`**: Lee los archivos `.xlsx` usando `openpyxl` en modo lectura (`read_only`) para eficiencia de memoria. Cierra los archivos inmediatamente para permitir su movimiento.
* **`src/transform.py`**:
    * Limpia datos y convierte tipos numéricos.
    * **Genera `Llave_Comun`**: (YYYYMMDDHHMM) para relacionar tablas.
    * **Estandariza Fechas**: Redondea tiempos a intervalos de 10 minutos.
    * **Codifica Pasillos**: Transforma "Pasillo 1" a "P001".
* **`src/load.py`**: Genera los CSVs consolidados y maneja la escritura segura.
* **`run_etl.py`**: El orquestador. Itera sobre los procesos configurados, gestiona el flujo de datos y mueve los archivos procesados a la carpeta `Archive`.

---

## 📂 Estructura de Directorios

El sistema requiere una estructura de carpetas específica para separar los insumos por tipo de proceso.

```text
Carpeta Raiz/ (Configurable)
├── Archive/                  # Destino de archivos procesados
│   ├── Pasillos/
│   ├── Muelles/
│   ├── Tuneles/
│   ├── Presion/
│   └── Compresores/
│
├── Export/                   # Salida de CSVs limpios
│   ├── consol_pasillos.csv
│   ├── consol_muelles.csv
│   ├── consol_tuneles.csv
│   ├── consol_presion.csv
│   └── consol_compresores.csv
│
├── Import/                   # Bandeja de entrada (Archivos .xlsx)
│   ├── Pasillos/
│   ├── Muelles/
│   ├── Tuneles/
│   ├── Presion/
│   └── Compresores/
⚙️ Configuración (config.json)
Es IMPERATIVO configurar las rutas en el archivo config.json ubicado en la raíz. El sistema soporta múltiples procesos simultáneos.

Ejemplo de configuración:

JSON

{
    "RUTAS_PROCESO": {
        "PASILLOS": {
            "INPUT": "C:\\Users\\Usuario\\DB_sitrad\\Import\\Pasillos\\",
            "OUTPUT_NAME": "consol_pasillos.csv"
        },
        "MUELLES": {
            "INPUT": "C:\\Users\\Usuario\\DB_sitrad\\Import\\Muelles\\",
            "OUTPUT_NAME": "consol_muelles.csv"
        },
        "TUNELES": {
            "INPUT": "C:\\Users\\Usuario\\DB_sitrad\\Import\\Tuneles\\",
            "OUTPUT_NAME": "consol_tuneles.csv"
        },
        "PRESION": {
            "INPUT": "C:\\Users\\Usuario\\DB_sitrad\\Import\\Presion\\",
            "OUTPUT_NAME": "consol_presion.csv"
        },
        "COMPRESORES": {
            "INPUT": "C:\\Users\\Usuario\\DB_sitrad\\Import\\Compresores\\",
            "OUTPUT_NAME": "consol_compresores.csv"
        }
    },
    "CARPETA_DESTINO_GENERAL": "C:\\Users\\Usuario\\DB_sitrad\\Export\\",
    "CARPETA_ARCHIVADOS_GENERAL": "C:\\Users\\Usuario\\DB_sitrad\\Archive\\"
}
✨ Nuevas Funcionalidades
El ETL ha sido actualizado con lógica de negocio avanzada:

Dinamismo de Esquemas: El sistema detecta automáticamente si el archivo es un Sensor, una lectura de Presión o un Compresor, y aplica las columnas de salida correspondientes.

Relacionamiento (Llave_Comun): Se genera automáticamente una columna concatenada Anio+Mes+Dia+Hora10min (ej: 202601160010) en todas las tablas para permitir cruces de datos precisos.

Normalización de Tiempo: Todas las horas se redondean al intervalo de 10 minutos más cercano (00:04 -> 00:00, 00:06 -> 00:10) para sincronizar eventos.

Codificación de Pasillos: Se crea la columna Pasillo_est que estandariza nombres (ej: "Pasillo 1" -> "P001", "Pulmón" -> "PULMON").

🛠️ Instalación y Ejecución
Requisitos Previos
Python 3.8+

Librería openpyxl

Paso 1: Configurar Entorno
Bash

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
.\venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate
Paso 2: Instalar Dependencias
Bash

pip install openpyxl
Paso 3: Ejecutar ETL
Coloca los archivos .xlsx en sus carpetas Import correspondientes y ejecuta:

Bash

python run_etl.py

