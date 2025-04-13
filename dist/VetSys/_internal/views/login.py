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
    root.geometry("350x200")
    root.configure(bg="#f4f6f9")

    tk.Label(
        root,
        text="Inicio de Sesión",
        font=("Segoe UI", 16, "bold"),
        bg="#f4f6f9",
        fg="#0d47a1",
    ).pack(pady=10)

    frame = tk.Frame(root, bg="#f4f6f9")
    frame.pack(pady=10)

    tk.Label(frame, text="Usuario:", bg="#f4f6f9").grid(
        row=0, column=0, padx=10, pady=5
    )
    entry_usuario = tk.Entry(frame)
    entry_usuario.grid(row=0, column=1)

    tk.Label(frame, text="Contraseña:", bg="#f4f6f9").grid(
        row=1, column=0, padx=10, pady=5
    )
    entry_clave = tk.Entry(frame, show="*")
    entry_clave.grid(row=1, column=1)

    tk.Button(
        root, text="Iniciar Sesión", font=("Segoe UI", 10), width=20, command=validar
    ).pack(pady=10)

    root.mainloop()
