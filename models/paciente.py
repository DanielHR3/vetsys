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
