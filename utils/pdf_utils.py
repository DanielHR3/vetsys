import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generar_receta_pdf(paciente, fecha, diagnostico, medicamentos, instrucciones):
    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(carpeta_descargas, exist_ok=True)

    nombre_archivo = f"receta_{paciente.replace(' ', '_')}_{fecha}.pdf"
    ruta = os.path.join(carpeta_descargas, nombre_archivo)

    c = canvas.Canvas(ruta, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(50, 750, f"Clínica Veterinaria - Receta Médica")
    c.drawString(50, 730, f"Paciente: {paciente}")
    c.drawString(50, 710, f"Fecha: {fecha}")
    c.drawString(50, 690, f"Diagnóstico: {diagnostico}")
    c.drawString(50, 670, "Medicamentos:")
    c.drawString(70, 650, medicamentos)
    c.drawString(50, 630, "Instrucciones:")
    c.drawString(70, 610, instrucciones)
    c.drawString(50, 100, "___________________________")
    c.drawString(50, 85, "Firma del médico")

    c.save()
    return ruta
def generar_historial_pdf(paciente, registros):
    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(carpeta_descargas, exist_ok=True)

    nombre_archivo = f"historial_{paciente.replace(' ', '_')}.pdf"
    ruta = os.path.join(carpeta_descargas, nombre_archivo)

    c = canvas.Canvas(ruta, pagesize=letter)
    c.setFont("Helvetica", 11)
    y = 750

    c.drawString(50, y, f"Historial Médico - {paciente}")
    y -= 30

    for r in registros:
        fecha, sintomas, diagnostico, tratamiento, observaciones = r[1:6]
        c.drawString(50, y, f"Fecha: {fecha}")
        c.drawString(50, y - 15, f"Síntomas: {sintomas}")
        c.drawString(50, y - 30, f"Diagnóstico: {diagnostico}")
        c.drawString(50, y - 45, f"Tratamiento: {tratamiento}")
        c.drawString(50, y - 60, f"Observaciones: {observaciones}")
        y -= 90
        if y < 100:
            c.showPage()
            y = 750

    c.drawString(50, 80, "___________________________")
    c.drawString(50, 65, "Firma del médico")

    c.save()
    return ruta

