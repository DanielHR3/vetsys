"""Script para crear la tabla 'recetas' si no existe en la base de datos VetSys."""

import sqlite3


def crear_tabla_recetas():
    """Crea la tabla 'recetas' en la base de datos VetSys si no existe."""
    # Asegúrate de que el nombre del archivo sea el mismo que usas en el resto del sistema
    con = sqlite3.connect(
        "VetSys.sqlite"
    )  # Puedes cambiarlo por la ruta real de tu .sqlite
    cur = con.cursor()

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
        );
    """
    )

    con.commit()
    con.close()
    print("✅ Tabla 'recetas' verificada o creada correctamente.")


if __name__ == "__main__":
    crear_tabla_recetas()
