import os
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry

from models.historial import agregar_historial, obtener_historial_por_paciente, editar_historial, eliminar_historial
from models.paciente import obtener_pacientes
from utils.pdf_utils import generar_historial_pdf


def volver_al_menu():
    from views.dashboard import mostrar_menu
    mostrar_menu()


def ventana_historial():
    historial_editando = {"id": None}

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

    def guardar_o_actualizar():
        paciente_nombre = combo_paciente.get()
        if not paciente_nombre:
            messagebox.showwarning("Selecciona un paciente", "Debes seleccionar un paciente.")
            return

        paciente_id = pacientes_dict[paciente_nombre]
        fecha = date_fecha.get()
        sintomas = entry_sintomas.get()
        diagnostico = entry_diagnostico.get()
        tratamiento = entry_tratamiento.get()
        observaciones = entry_observaciones.get()

        if historial_editando["id"]:
            editar_historial(historial_editando["id"], paciente_id, fecha, sintomas, diagnostico, tratamiento, observaciones)
            messagebox.showinfo("Actualizado", "El registro fue actualizado correctamente.")
            btn_guardar.config(text="Guardar Historial")
            historial_editando["id"] = None
        else:
            agregar_historial(paciente_id, fecha, sintomas, diagnostico, tratamiento, observaciones)
            messagebox.showinfo("Historial registrado", "El historial fue registrado correctamente.")

        limpiar_campos()
        cargar_historial()

    def llenar_formulario(event):
        seleccionado = tabla.selection()
        if not seleccionado:
            return
        datos = tabla.item(seleccionado)["values"]
        historial_editando["id"] = datos[0]
        date_fecha.set_date(datos[1])
        entry_sintomas.delete(0, tk.END)
        entry_sintomas.insert(0, datos[2])
        entry_diagnostico.delete(0, tk.END)
        entry_diagnostico.insert(0, datos[3])
        entry_tratamiento.delete(0, tk.END)
        entry_tratamiento.insert(0, datos[4])
        entry_observaciones.delete(0, tk.END)
        entry_observaciones.insert(0, datos[5])
        btn_guardar.config(text="Actualizar Historial")

    def eliminar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Selecciona", "Debes seleccionar un registro.")
            return
        datos = tabla.item(seleccionado)["values"]
        confirm = messagebox.askyesno("Eliminar", "¿Eliminar este registro del historial?")
        if confirm:
            eliminar_historial(datos[0])
            cargar_historial()
            limpiar_campos()
            messagebox.showinfo("Eliminado", "Registro eliminado correctamente.")

    def limpiar_campos():
        entry_sintomas.delete(0, tk.END)
        entry_diagnostico.delete(0, tk.END)
        entry_tratamiento.delete(0, tk.END)
        entry_observaciones.delete(0, tk.END)
        historial_editando["id"] = None
        btn_guardar.config(text="Guardar Historial")

    def exportar_historial():
        paciente_nombre = combo_paciente.get()
        if not paciente_nombre:
            messagebox.showwarning("Advertencia", "Debes seleccionar un paciente.")
            return

        paciente_id = pacientes_dict[paciente_nombre]
        registros = obtener_historial_por_paciente(paciente_id)
        if not registros:
            messagebox.showinfo("Sin registros", "Este paciente no tiene historial médico.")
            return

        try:
            ruta = generar_historial_pdf(paciente_nombre, registros)
            messagebox.showinfo("PDF generado", f"Historial exportado como PDF:\n{ruta}")

            if platform.system() == "Windows":
                os.startfile(ruta)
            elif platform.system() == "Darwin":
                subprocess.call(["open", ruta])
            else:
                subprocess.call(["xdg-open", ruta])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")

    # VENTANA
    win = tk.Tk()
    win.title("VetSys - Historial Médico")
    win.geometry("980x600")
    win.configure(bg="#e8f0fe")

    tk.Label(win, text="Historial Médico", font=("Segoe UI", 18, "bold"), bg="#e8f0fe", fg="#0d47a1").pack(pady=10)

    form = tk.Frame(win, bg="#e8f0fe")
    form.pack(pady=10)

    pacientes = obtener_pacientes()
    pacientes_dict = {f"{p[1]} (ID {p[0]})": p[0] for p in pacientes}
    tk.Label(form, text="Paciente", bg="#e8f0fe").grid(row=0, column=0, padx=5, pady=5)
    combo_paciente = ttk.Combobox(form, values=list(pacientes_dict.keys()), width=30)
    combo_paciente.grid(row=0, column=1, padx=10)

    tk.Label(form, text="Fecha", bg="#e8f0fe").grid(row=0, column=2)
    date_fecha = DateEntry(form, width=15, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
    date_fecha.grid(row=0, column=3, padx=10)

    campos = [
        ("Síntomas", 1, 0, "entry_sintomas"),
        ("Diagnóstico", 1, 2, "entry_diagnostico"),
        ("Tratamiento", 2, 0, "entry_tratamiento"),
        ("Observaciones", 2, 2, "entry_observaciones"),
    ]
    for texto, fila, col, _ in campos:
        tk.Label(form, text=texto, bg="#e8f0fe").grid(row=fila, column=col, padx=5, pady=5)

    entry_sintomas = tk.Entry(form, width=30)
    entry_diagnostico = tk.Entry(form, width=30)
    entry_tratamiento = tk.Entry(form, width=30)
    entry_observaciones = tk.Entry(form, width=30)

    entry_sintomas.grid(row=1, column=1)
    entry_diagnostico.grid(row=1, column=3)
    entry_tratamiento.grid(row=2, column=1)
    entry_observaciones.grid(row=2, column=3)

    btn_frame = tk.Frame(win, bg="#e8f0fe")
    btn_frame.pack(pady=10)

    btn_guardar = tk.Button(btn_frame, text="Guardar Historial", width=20, command=guardar_o_actualizar)
    btn_guardar.pack(side=tk.LEFT, padx=10)

    tk.Button(btn_frame, text="Eliminar", width=20, command=eliminar).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Exportar Historial a PDF", width=25, command=exportar_historial).pack(side=tk.LEFT, padx=10)

    tk.Button(
        win, text="Volver al Menú", width=20, bg="#dfefff", command=lambda: [win.destroy(), volver_al_menu()]
    ).pack(pady=10)

    tabla = ttk.Treeview(
        win,
        columns=("ID", "Fecha", "Síntomas", "Diagnóstico", "Tratamiento", "Observaciones"),
        show="headings",
        height=10
    )
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=130)
    tabla.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
    tabla.bind("<<TreeviewSelect>>", llenar_formulario)

    combo_paciente.bind("<<ComboboxSelected>>", lambda e: cargar_historial())
    win.mainloop()
