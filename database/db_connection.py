import sqlite3


def conectar():
    conexion = sqlite3.connect("database/vetsys.db")
    return conexion
