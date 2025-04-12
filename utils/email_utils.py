import os

import yagmail

# Correo emisor (el tuyo)
EMAIL = "danielhrubio3@gmail.com"
PASSWORD = "ftse kior witw irhn "  # Sugerido: usar una app password


def enviar_correo(destinatario, paciente, fecha, hora, motivo, archivo_ics=None):
    try:
        yag = yagmail.SMTP(EMAIL, PASSWORD)
        asunto = "Confirmación de Cita Veterinaria"
        contenido = f"""
Hola,

Tu cita para {paciente} ha sido registrada con éxito:

📅 Fecha: {fecha}
⏰ Hora: {hora}
📌 Motivo: {motivo}

Adjunto encontrarás el archivo para añadir esta cita a tu calendario.

Gracias por confiar en nosotros.
"""
        adjuntos = (
            [archivo_ics] if archivo_ics and os.path.exists(archivo_ics) else None
        )
        yag.send(destinatario, asunto, contenido, attachments=adjuntos)
        return True
    except Exception as e:
        print("Error al enviar correo:", e)
        return False
