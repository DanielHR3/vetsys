"""Módulo para generar recetas médicas en formato PDF en VetSys."""

import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generar_receta_pdf(
    paciente_nombre, fecha, diagnostico, medicamentos, instrucciones
):
    """Genera un PDF con los datos de la receta médica y espacio para firma manual."""

    # Crea carpeta si no existe
    os.makedirs("recetas_pdf", exist_ok=True)

    # Nombre del archivo con fecha
    filename = f"recetas_pdf/receta_{paciente_nombre.replace(' ', '_')}_{fecha}.pdf"

    c = canvas.Canvas(filename, pagesize=letter)
    _, height = letter

    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Receta Médica")

    # Datos del paciente
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Paciente: {paciente_nombre}")
    c.drawString(50, height - 120, f"Fecha: {fecha}")
    c.drawString(50, height - 140, "Diagnóstico:")
    text_diag = c.beginText(50, height - 160)
    text_diag.textLines(diagnostico)
    c.drawText(text_diag)

    # Medicamentos
    c.drawString(50, height - 220, "Medicamentos:")
    text_med = c.beginText(50, height - 240)
    text_med.textLines(medicamentos)
    c.drawText(text_med)

    # Instrucciones
    c.drawString(50, height - 320, "Instrucciones:")
    text_inst = c.beginText(50, height - 340)
    text_inst.textLines(instrucciones)
    c.drawText(text_inst)

    # Firma manual
    c.drawString(50, 100, "____________________________")
    c.drawString(50, 85, "Firma del médico")

    c.save()
    return filename
