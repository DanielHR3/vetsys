import tkinter as tk
from tkinter import messagebox

from database.db_connection import conectar


def iniciar_sesion():
    def validar():
        usuario = entry_usuario.get()
        clave = entry_clave.get()
        if usuario == "admin" and clave == "admin":
            messagebox.showinfo("Acceso permitido", "¡Bienvenido al sistema VetSys!")
            root.destroy()
            from views.dashboard import mostrar_menu

            mostrar_menu()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    root = tk.Tk()
    root.title("VetSys - Inicio de Sesión")
    root.geometry("300x150")

    tk.Label(root, text="Usuario:").grid(row=0, column=0, padx=10, pady=10)
    entry_usuario = tk.Entry(root)
    entry_usuario.grid(row=0, column=1)

    tk.Label(root, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
    entry_clave = tk.Entry(root, show="*")
    entry_clave.grid(row=1, column=1)

    tk.Button(root, text="Iniciar Sesión", command=validar).grid(
        row=2, column=0, columnspan=2, pady=10
    )

    root.mainloop()
