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


def editar_cita(id_cita, paciente_id, fecha, hora, motivo):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        UPDATE citas
        SET paciente_id = ?, fecha = ?, hora = ?, motivo = ?
        WHERE id = ?
    """,
        (paciente_id, fecha, hora, motivo, id_cita),
    )
    con.commit()
    con.close()


def eliminar_cita(id_cita):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM citas WHERE id = ?", (id_cita,))
    con.commit()
    con.close()
