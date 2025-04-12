import os
from datetime import datetime

from icalendar import Calendar, Event


def generar_archivo_calendario(paciente, fecha, hora, motivo):
    cal = Calendar()
    evento = Event()

    # Convertimos fecha y hora en datetime
    fecha_inicio = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    fecha_fin = fecha_inicio.replace(
        minute=fecha_inicio.minute + 30
    )  # duración estimada

    evento.add("summary", f"Cita veterinaria - {paciente}")
    evento.add("dtstart", fecha_inicio)
    evento.add("dtend", fecha_fin)
    evento.add("description", motivo)
    evento.add("location", "Clínica Veterinaria")
    evento.add("status", "CONFIRMED")

    cal.add_component(evento)

    ruta_archivo = f"cita_{paciente.replace(' ', '_')}.ics"
    with open(ruta_archivo, "wb") as f:
        f.write(cal.to_ical())

    return ruta_archivo
