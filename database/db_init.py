from database.db_connection import conectar


def crear_tabla_inventario():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            descripcion TEXT
        )
    """
    )
    con.commit()
    con.close()
    print("✅ Tabla 'inventario' creada correctamente.")


crear_tabla_inventario()
