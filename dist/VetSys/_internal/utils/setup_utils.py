import os

from database.db_migration import migrar_base_de_datos
from database.db_connection import conectar


def inicializar_base_datos():
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "vetsys.db")
    if not os.path.exists(db_path):
        print("📁 Base de datos NO encontrada, creando nueva...")
    else:
        print("📁 Base de datos existente detectada.")
    migrar_base_de_datos()
    con = conectar()
    cur = con.cursor()

    # Crear tabla pacientes
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            especie TEXT,
            raza TEXT,
            sexo TEXT,
            fecha_nacimiento TEXT,
            propietario TEXT,
            contacto TEXT
        )"""
    )

    # Crear tabla citas
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            fecha TEXT,
            hora TEXT,
            motivo TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )"""
    )

    # Crear tabla recetas
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS recetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            fecha TEXT,
            diagnostico TEXT,
            medicamentos TEXT,
            instrucciones TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )"""
    )

    # Crear tabla inventario
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
        )"""
    )

    con.commit()
    con.close()
    print("✅ Base de datos creada correctamente.")
