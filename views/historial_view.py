import tkinter as tk
from tkinter import messagebox, ttk

from tkcalendar import DateEntry

from models.historial import agregar_historial, obtener_historial_por_paciente
from models.paciente import obtener_pacientes


def volver_al_menu():
    from views.dashboard import mostrar_menu

    mostrar_menu()


def ventana_historial():
    def cargar_historial():
        paciente_nombre = combo_paciente.get()
        if not paciente_nombre:
            return
        paciente_id = pacientes_dict[paciente_nombre]
        registros = obtener_historial_por_paciente(paciente_id)

        for row in tabla.get_children():
            tabla.delete(row)

        for r in registros:
            tabla.insert("", "end", values=r)

    def guardar():
        paciente_nombre = combo_paciente.get()
        if not paciente_nombre:
            messagebox.showwarning(
                "Selecciona un paciente", "Debes seleccionar un paciente."
            )
            return
        paciente_id = pacientes_dict[paciente_nombre]
        agregar_historial(
            paciente_id,
            date_fecha.get(),
            entry_sintomas.get(),
            entry_diagnostico.get(),
            entry_tratamiento.get(),
            entry_observaciones.get(),
        )
        limpiar_campos()
        cargar_historial()
        messagebox.showinfo(
            "Historial registrado", "El historial médico fue registrado correctamente."
        )

    def limpiar_campos():
        entry_sintomas.delete(0, tk.END)
        entry_diagnostico.delete(0, tk.END)
        entry_tratamiento.delete(0, tk.END)
        entry_observaciones.delete(0, tk.END)

    win = tk.Tk()
    win.title("VetSys - Historial Médico")
    win.geometry("900x550")
    win.configure(bg="#f4f6f9")

    tk.Label(
        win, text="Historial Médico", font=("Arial", 16, "bold"), bg="#f4f6f9"
    ).pack(pady=10)

    form = tk.Frame(win, bg="#f4f6f9")
    form.pack(pady=10)

    pacientes = obtener_pacientes()
    pacientes_dict = {f"{p[1]} (ID {p[0]})": p[0] for p in pacientes}
    combo_paciente = ttk.Combobox(form, values=list(pacientes_dict.keys()), width=30)
    combo_paciente.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(form, text="Paciente", bg="#f4f6f9").grid(row=0, column=0, padx=5, pady=5)

    date_fecha = DateEntry(
        form,
        width=15,
        background="darkblue",
        foreground="white",
        date_pattern="yyyy-mm-dd",
    )
    date_fecha.grid(row=0, column=3, padx=10)
    tk.Label(form, text="Fecha", bg="#f4f6f9").grid(row=0, column=2)

    labels = [
        ("Síntomas", 1, 0),
        ("Diagnóstico", 1, 2),
        ("Tratamiento", 2, 0),
        ("Observaciones", 2, 2),
    ]
    for text, row, col in labels:
        tk.Label(form, text=text, bg="#f4f6f9").grid(
            row=row, column=col, padx=5, pady=5
        )

    entry_sintomas = tk.Entry(form, width=30)
    entry_diagnostico = tk.Entry(form, width=30)
    entry_tratamiento = tk.Entry(form, width=30)
    entry_observaciones = tk.Entry(form, width=30)

    entry_sintomas.grid(row=1, column=1)
    entry_diagnostico.grid(row=1, column=3)
    entry_tratamiento.grid(row=2, column=1)
    entry_observaciones.grid(row=2, column=3)

    tk.Button(form, text="Guardar Historial", command=guardar, width=20).grid(
        row=3, columnspan=4, pady=10
    )
    tk.Button(
        win,
        text="Volver al Menú",
        width=20,
        bg="#dfefff",
        command=lambda: [win.destroy(), volver_al_menu()],
    ).pack(pady=10)

    # Tabla de historial
    tabla = ttk.Treeview(
        win,
        columns=(
            "ID",
            "Fecha",
            "Síntomas",
            "Diagnóstico",
            "Tratamiento",
            "Observaciones",
        ),
        show="headings",
    )
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=120)
    tabla.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

    # Cargar historial al seleccionar paciente
    combo_paciente.bind("<<ComboboxSelected>>", lambda e: cargar_historial())

    win.mainloop()
