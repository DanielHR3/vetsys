from utils.setup_utils import inicializar_base_datos
from views.login import iniciar_sesion

if __name__ == "__main__":
    # Ejecutar la inicialización al inicio del programa
    inicializar_base_datos()

    # Luego se muestra el login
    iniciar_sesion()
