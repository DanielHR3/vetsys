"""Módulo de vista para registrar y consultar recetas médicas en VetSys."""

import tkinter as tk
from tkinter import messagebox, ttk

from tkcalendar import DateEntry

from models.paciente import obtener_pacientes
from models.receta import guardar_receta, obtener_recetas_por_paciente


def volver_al_menu():
    """Regresa al menú principal."""
    from views.dashboard import \
        mostrar_menu  # pylint: disable=import-outside-toplevel

    mostrar_menu()


def ventana_recetas():
    """Crea la interfaz para agregar y consultar recetas médicas."""

    def cargar_recetas():
        """Carga las recetas del paciente seleccionado."""
        paciente_nombre = combo_paciente.get()
        if not paciente_nombre:
            return
        paciente_id = pacientes_dict[paciente_nombre]
        registros = obtener_recetas_por_paciente(paciente_id)

        for row in tabla.get_children():
            tabla.delete(row)

        for r in registros:
            tabla.insert("", "end", values=r)

    def guardar():
        """Guarda una receta para el paciente seleccionado."""
        paciente_nombre = combo_paciente.get()
        if not paciente_nombre:
            messagebox.showwarning("Advertencia", "Debes seleccionar un paciente.")
            return
        paciente_id = pacientes_dict[paciente_nombre]
        try:
            guardar_receta(
                paciente_id,
                date_fecha.get(),
                entry_diagnostico.get(),
                txt_medicamentos.get("1.0", tk.END).strip(),
                txt_instrucciones.get("1.0", tk.END).strip(),
            )
            limpiar_campos()
            cargar_recetas()
            messagebox.showinfo(
                "Receta guardada", "La receta fue registrada correctamente."
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            messagebox.showerror("Error", f"No se pudo guardar la receta: {e}")

    def limpiar_campos():
        """Limpia todos los campos del formulario."""
        entry_diagnostico.delete(0, tk.END)
        txt_medicamentos.delete("1.0", tk.END)
        txt_instrucciones.delete("1.0", tk.END)

    win = tk.Tk()
    win.title("VetSys - Recetas Médicas")
    win.geometry("900x600")
    win.configure(bg="#f4f6f9")

    tk.Label(
        win, text="Recetas Médicas", font=("Arial", 16, "bold"), bg="#f4f6f9"
    ).pack(pady=10)

    form = tk.Frame(win, bg="#f4f6f9")
    form.pack(pady=10)

    pacientes = obtener_pacientes()
    pacientes_dict = {f"{p[1]} (ID {p[0]})": p[0] for p in pacientes}
    combo_paciente = ttk.Combobox(form, values=list(pacientes_dict.keys()), width=30)
    combo_paciente.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(form, text="Paciente", bg="#f4f6f9").grid(row=0, column=0)

    date_fecha = DateEntry(
        form,
        width=15,
        background="darkblue",
        foreground="white",
        date_pattern="yyyy-mm-dd",
    )
    date_fecha.grid(row=0, column=3)
    tk.Label(form, text="Fecha", bg="#f4f6f9").grid(row=0, column=2)

    tk.Label(form, text="Diagnóstico", bg="#f4f6f9").grid(row=1, column=0, pady=5)
    entry_diagnostico = tk.Entry(form, width=40)
    entry_diagnostico.grid(row=1, column=1, columnspan=3, padx=5)

    tk.Label(form, text="Medicamentos", bg="#f4f6f9").grid(row=2, column=0, pady=5)
    txt_medicamentos = tk.Text(form, width=70, height=4)
    txt_medicamentos.grid(row=2, column=1, columnspan=3, padx=5)

    tk.Label(form, text="Instrucciones", bg="#f4f6f9").grid(row=3, column=0, pady=5)
    txt_instrucciones = tk.Text(form, width=70, height=4)
    txt_instrucciones.grid(row=3, column=1, columnspan=3, padx=5)
    tk.Button(form, text="Guardar Receta", width=20, command=guardar).grid(
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
    tabla = ttk.Treeview(
        win,
        columns=("ID", "Fecha", "Diagnóstico", "Medicamentos", "Instrucciones"),
        show="headings",
    )
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

    combo_paciente.bind("<<ComboboxSelected>>", lambda e: cargar_recetas())
    win.mainloop()
