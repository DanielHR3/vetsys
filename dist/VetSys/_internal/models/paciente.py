from database.db_connection import conectar


def agregar_paciente(nombre, especie, raza, sexo, nacimiento, propietario, contacto):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO pacientes (nombre, especie, raza, sexo, fecha_nacimiento, propietario, contacto)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (nombre, especie, raza, sexo, nacimiento, propietario, contacto),
    )
    con.commit()
    con.close()


def obtener_pacientes():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM pacientes")
    resultados = cur.fetchall()
    con.close()
    return resultados


def editar_paciente(
    id_paciente, nombre, especie, raza, sexo, nacimiento, propietario, contacto
):
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        UPDATE pacientes
        SET nombre = ?, especie = ?, raza = ?, sexo = ?, fecha_nacimiento = ?, propietario = ?, contacto = ?
        WHERE id = ?
    """,
        (nombre, especie, raza, sexo, nacimiento, propietario, contacto, id_paciente),
    )
    con.commit()
    con.close()


def eliminar_paciente(id_paciente):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
    con.commit()
    con.close()
