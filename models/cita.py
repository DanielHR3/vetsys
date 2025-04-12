from database.db_connection import conectar


def guardar_cita(paciente_id, fecha, hora, motivo, correo):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO citas (paciente_id, fecha, hora, motivo)
        VALUES (?, ?, ?, ?)
    """,
        (paciente_id, fecha, hora, motivo),
    )
    con.commit()
    con.close()
    return True


def obtener_citas():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        SELECT citas.id, pacientes.nombre, citas.fecha, citas.hora, citas.motivo
        FROM citas
        JOIN pacientes ON pacientes.id = citas.paciente_id
    """
    )
    citas = cur.fetchall()
    con.close()
    return citas
