"""Módulo para gestionar el historial médico de los pacientes."""

from database.db_connection import conectar


def agregar_historial(
    paciente_id, fecha, sintomas, diagnostico, tratamiento, observaciones
):
    """Agrega un nuevo registro al historial médico del paciente."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO historial (paciente_id, fecha, sintomas, diagnostico, tratamiento, observaciones)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (paciente_id, fecha, sintomas, diagnostico, tratamiento, observaciones),
    )
    con.commit()
    con.close()


def obtener_historial_por_paciente(paciente_id):
    """Obtiene todos los registros de historial médico asociados a un paciente."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        SELECT id, fecha, sintomas, diagnostico, tratamiento, observaciones
        FROM historial
        WHERE paciente_id = ?
        ORDER BY fecha DESC
    """,
        (paciente_id,),
    )
    resultados = cur.fetchall()
    con.close()
    return resultados
