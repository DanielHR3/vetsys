"""Módulo de modelo para gestionar las recetas médicas de VetSys."""

from database.db_connection import conectar


def guardar_receta(paciente_id, fecha, diagnostico, medicamentos, instrucciones):
    """Guarda una receta médica en la base de datos."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO recetas (
            paciente_id, fecha, diagnostico, medicamentos, instrucciones
        ) VALUES (?, ?, ?, ?, ?)
        """,
        (paciente_id, fecha, diagnostico, medicamentos, instrucciones),
    )
    con.commit()
    con.close()


def obtener_recetas_por_paciente(paciente_id):
    """Obtiene todas las recetas médicas de un paciente."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        SELECT id, fecha, diagnostico, medicamentos, instrucciones
        FROM recetas
        WHERE paciente_id = ?
        ORDER BY fecha DESC
        """,
        (paciente_id,),
    )
    recetas = cur.fetchall()
    con.close()
    return recetas
