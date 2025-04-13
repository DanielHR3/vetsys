import tkinter as tk
from views.pacientes_view import ventana_pacientes
from views.citas_view import ventana_citas
from views.historial_view import ventana_historial
from views.recetas_view import ventana_recetas
from views.inventario_view import ventana_inventario
from utils.backup_utils import respaldar_base_datos
from tkinter import messagebox

def mostrar_menu():
    root = tk.Tk()
    root.title("VetSys - Menú Principal")
    root.geometry("600x600")  # Aumentamos altura
    root.configure(bg="#f4f6f9")

    tk.Label(root, text="VetSys", font=("Segoe UI", 24, "bold"), bg="#f4f6f9", fg="#0d47a1").pack(pady=20)
    tk.Label(root, text="Sistema de gestión veterinaria", font=("Segoe UI", 12), bg="#f4f6f9").pack()

    menu_frame = tk.Frame(root, bg="#f4f6f9")
    menu_frame.pack(pady=30)

    botones = [
        ("Pacientes", ventana_pacientes, "#00b894"),
        ("Citas", ventana_citas, "#0984e3"),
        ("Historial Médico", ventana_historial, "#6c5ce7"),
        ("Recetas", ventana_recetas, "#fdcb6e"),
        ("Inventario", ventana_inventario, "#e17055"),
    ]

    for idx, (texto, funcion, color) in enumerate(botones):
        tk.Button(
            menu_frame,
            text=texto,
            width=25,
            height=2,
            bg=color,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            command=lambda f=funcion: [root.destroy(), f()]
        ).pack(pady=6)

    # Botones extra
    extras = tk.Frame(root, bg="#f4f6f9")
    extras.pack(pady=30)

    tk.Button(
        extras,
        text="Respaldar BD",
        width=18,
        bg="#636e72",
        fg="white",
        font=("Segoe UI", 10),
        command=respaldar_y_notificar
    ).pack(side=tk.LEFT, padx=10)

    tk.Button(
        extras,
        text="Salir",
        width=18,
        bg="#d63031",
        fg="white",
        font=("Segoe UI", 10),
        command=root.destroy
    ).pack(side=tk.LEFT, padx=10)

    root.mainloop()

def respaldar_y_notificar():
    ruta = respaldar_base_datos()
    messagebox.showinfo("Respaldo completo", f"Respaldo guardado en:\n{ruta}")
