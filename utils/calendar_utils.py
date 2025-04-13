import os
from datetime import datetime, timedelta
from icalendar import Calendar, Event

def generar_archivo_calendario(paciente, fecha, hora, motivo):
    cal = Calendar()
    evento = Event()

    # Convertimos fecha y hora en datetime con validación robusta
    try:
        fecha_inicio = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    except ValueError as e:
        raise ValueError(f"Formato de fecha u hora inválido: {e}")

    # Duración estimada de 30 minutos
    fecha_fin = fecha_inicio + timedelta(minutes=30)

    evento.add("summary", f"Cita veterinaria - {paciente}")
    evento.add("dtstart", fecha_inicio)
    evento.add("dtend", fecha_fin)
    evento.add("description", motivo)
    evento.add("location", "Clínica Veterinaria")
    evento.add("status", "CONFIRMED")

    cal.add_component(evento)

    # Carpeta de descargas
    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(carpeta_descargas, exist_ok=True)

    # Nombre del archivo limpio
    nombre_archivo = f"cita_{paciente.replace(' ', '_')}.ics"
    ruta_archivo = os.path.join(carpeta_descargas, nombre_archivo)

    with open(ruta_archivo, "wb") as f:
        f.write(cal.to_ical())

    return ruta_archivo
