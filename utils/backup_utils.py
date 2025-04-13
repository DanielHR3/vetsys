import os
import shutil
from datetime import datetime

def respaldar_base_datos():
    origen = os.path.join(os.path.dirname(__file__), '..', 'database', 'vetsys.db')
    origen = os.path.abspath(origen)

    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(carpeta_descargas, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(carpeta_descargas, f"vetsys_backup_{timestamp}.db")

    shutil.copy(origen, destino)
    return destino
