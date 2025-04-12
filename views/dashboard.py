"""Módulo principal de menú del sistema VetSys."""

import tkinter as tk

from views.citas_view import ventana_citas
from views.historial_view import ventana_historial
from views.pacientes_view import ventana_pacientes


def mostrar_menu():
    """Muestra el menú principal con navegación a los diferentes módulos del sistema."""
    root = tk.Tk()
    root.title("VetSys - Menú Principal")
    root.geometry("350x300")
    root.configure(bg="#f0f4f8")

    tk.Label(
        root, text="🐾 VetSys", font=("Arial", 20, "bold"), bg="#f0f4f8", fg="#333"
    ).pack(pady=10)
    tk.Label(
        root,
        text="Bienvenido al sistema de gestión veterinaria",
        font=("Arial", 10),
        bg="#f0f4f8",
    ).pack(pady=5)

    frame = tk.Frame(root, bg="#f0f4f8")
    frame.pack(pady=20)

    tk.Button(
        frame,
        text="👤 Pacientes",
        width=25,
        font=("Arial", 12),
        command=lambda: [root.destroy(), ventana_pacientes()],
    ).pack(pady=10)

    tk.Button(
        frame,
        text="📅 Citas",
        width=25,
        font=("Arial", 12),
        command=lambda: [root.destroy(), ventana_citas()],
    ).pack(pady=10)

    tk.Button(
        frame,
        text="📋 Historial Médico",
        width=25,
        font=("Arial", 12),
        command=lambda: [root.destroy(), ventana_historial()],
    ).pack(pady=10)

    tk.Button(
        root, text="🚪 Salir", width=20, font=("Arial", 10), command=root.destroy
    ).pack(pady=10)

    root.mainloop()
