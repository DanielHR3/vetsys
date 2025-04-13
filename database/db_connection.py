import sqlite3
import os

def conectar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "vetsys.db")
    print(f"✅ Conectado a: {db_path}")
    return sqlite3.connect(db_path)

