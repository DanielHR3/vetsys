import tkinter as tk
from tkinter import messagebox, ttk

from tkcalendar import DateEntry

from models.paciente import agregar_paciente, obtener_pacientes


def volver_al_menu():
    from views.dashboard import mostrar_menu

    mostrar_menu()


def ventana_pacientes():
    def agregar():
        agregar_paciente(
            entry_nombre.get(),
            entry_especie.get(),
            entry_raza.get(),
            entry_sexo.get(),
            entry_nacimiento.get(),
            entry_propietario.get(),
            entry_contacto.get(),
        )
        actualizar_tabla()
        limpiar_campos()
        messagebox.showinfo(
            "Paciente agregado", "El paciente fue registrado correctamente."
        )

    def actualizar_tabla():
        for row in tree.get_children():
            tree.delete(row)
        for paciente in obtener_pacientes():
            tree.insert("", "end", values=paciente)

    def limpiar_campos():
        entry_nombre.delete(0, tk.END)
        entry_especie.delete(0, tk.END)
        entry_raza.delete(0, tk.END)
        entry_sexo.delete(0, tk.END)
        entry_nacimiento.set_date("")
        entry_propietario.delete(0, tk.END)
        entry_contacto.delete(0, tk.END)

    win = tk.Tk()
    win.title("VetSys - Pacientes")
    win.geometry("900x550")
    win.configure(bg="#f4f6f9")

    tk.Label(
        win, text="Gestión de Pacientes", font=("Arial", 16, "bold"), bg="#f4f6f9"
    ).pack(pady=10)

    frame = tk.Frame(win, bg="#f4f6f9")
    frame.pack(pady=10)

    # Labels
    labels = [
        ("Nombre", 0, 0),
        ("Especie", 0, 2),
        ("Raza", 1, 0),
        ("Sexo", 1, 2),
        ("Nacimiento", 2, 0),
        ("Propietario", 2, 2),
        ("Contacto", 3, 0),
    ]

    for text, row, col in labels:
        tk.Label(frame, text=text, bg="#f4f6f9").grid(
            row=row, column=col, padx=5, pady=5
        )

    # Entradas
    entry_nombre = tk.Entry(frame, width=30)
    entry_especie = tk.Entry(frame, width=30)
    entry_raza = tk.Entry(frame, width=30)
    entry_sexo = tk.Entry(frame, width=30)
    entry_nacimiento = DateEntry(
        frame,
        width=27,
        background="darkblue",
        foreground="white",
        date_pattern="yyyy-mm-dd",
    )
    entry_propietario = tk.Entry(frame, width=30)
    entry_contacto = tk.Entry(frame, width=30)

    widgets = [
        (entry_nombre, 0, 1),
        (entry_especie, 0, 3),
        (entry_raza, 1, 1),
        (entry_sexo, 1, 3),
        (entry_nacimiento, 2, 1),
        (entry_propietario, 2, 3),
        (entry_contacto, 3, 1),
    ]

    for widget, row, col in widgets:
        widget.grid(row=row, column=col, padx=5, pady=5)

    # Botones
    tk.Button(frame, text="Agregar Paciente", command=agregar, width=20).grid(
        row=4, columnspan=4, pady=10
    )
    tk.Button(
        win,
        text="Volver al Menú",
        width=20,
        bg="#dfefff",
        command=lambda: [win.destroy(), volver_al_menu()],
    ).pack(pady=10)

    # Tabla
    tree = ttk.Treeview(
        win,
        columns=(
            "ID",
            "Nombre",
            "Especie",
            "Raza",
            "Sexo",
            "Nacimiento",
            "Propietario",
            "Contacto",
        ),
        show="headings",
    )
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=110)
    tree.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

    actualizar_tabla()
    win.mainloop()
