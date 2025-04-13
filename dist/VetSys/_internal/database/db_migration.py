import os
import sqlite3


def conectar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "vetsys.db")
    return sqlite3.connect(db_path)


def agregar_columna_si_no_existe(cursor, tabla, columna, tipo):
    try:
        cursor.execute(f"SELECT {columna} FROM {tabla} LIMIT 1")
    except sqlite3.OperationalError:
        print(f"➕ Agregando columna '{columna}' a la tabla '{tabla}'")
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo}")


def migrar_base_de_datos():
    con = conectar()
    cur = con.cursor()

    # Crear tabla inventario con todas las columnas necesarias
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            marca TEXT,
            submarca TEXT,
            sku TEXT,
            codigo_barras TEXT,
            unidad TEXT,
            precio REAL,
            categoria TEXT,
            subcategoria TEXT,
            descripcion TEXT,
            imagen TEXT
        )
    """
    )

    # Asegurar columnas adicionales para historial
    agregar_columna_si_no_existe(cur, "historial", "peso", "REAL")
    agregar_columna_si_no_existe(cur, "historial", "temperatura", "REAL")
    agregar_columna_si_no_existe(cur, "historial", "condicion_corporal", "TEXT")
    agregar_columna_si_no_existe(cur, "historial", "presion_arterial", "TEXT")
    agregar_columna_si_no_existe(cur, "historial", "signos_vitales", "TEXT")

    # Asegurar columna diagnostico en recetas
    agregar_columna_si_no_existe(cur, "recetas", "diagnostico", "TEXT")

    con.commit()
    con.close()
    print("✅ Migración completa.")
